import json
from pyannote.audio import Pipeline
from pydub import AudioSegment
from pydub.utils import make_chunks
import concurrent.futures
import whisper
import os
from time import perf_counter
import torchaudio
from torchaudio import functional as F
from pydub.silence import split_on_silence
import pydub.silence as silence
import multiprocessing
from processor.translate_subtitle import toSub
#import threading

class toText:
    SAMPLE_RATE = 16000

    def __init__(self, id, audio, original_language, target_language):
        self.id = id
        self.audio = audio
        self.original = original_language
        self.target = target_language
        self.diarization_pipeline = Pipeline.from_pretrained(
            checkpoint_path="pyannote/speaker-diarization-3.1",  # Ruta al modelo preentrenado para la diarización de hablantes
            use_auth_token='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',  # Token de autenticación para la descarga del modelo
        )

        self.whisper_model = whisper.load_model('medium')
        self.sub = toSub(self.id, self.original, self.target)

        self.processed_chunks = set()
        self.transcribe_chunks()

    def transcribe_chunks(self):
        try:
            output_dir = "./temp/"  # Directorio de salida para archivos temporales
            os.makedirs(output_dir, exist_ok=True)  # Crea el directorio si no existe

            audio_segment = AudioSegment.from_file(self.audio)  # Carga el archivo de audio
            audio_duration = len(audio_segment) / 1000  # Calcula la duración del audio en segundos

            if audio_duration < 60:  # Si el audio es demasiado corto
                print("Audio is too short.")
                self.transcribe(self.audio, 0)  # Transcribe el audio completo
                self.sub.toSubtitle()  # Traduce los subtítulos
            else:
                # Detecta los silencios en el audio
                silent_ranges = silence.detect_silence(audio_segment, min_silence_len=5000, silence_thresh=-40)

                chunk_start_times = [0]  # Lista para almacenar los tiempos de inicio de los trozos

                
                for silent_range in silent_ranges:
                    start_time, end_time = silent_range
                    # Convertir a segundos y agregar al inicio del siguiente chunk
                    chunk_start_times.append(end_time / 1000)
                
                # Convertir los tiempos de inicio de los chunks en milisegundos para make_chunks
                chunk_start_times_ms = [int(time * 1000) for time in chunk_start_times]
                
                # Crear chunks basados en los tiempos de inicio calculados
                chunks = []
                for i in range(len(chunk_start_times_ms) - 1):
                    chunk = audio_segment[chunk_start_times_ms[i]:chunk_start_times_ms[i + 1]]
                    chunks.append(chunk)

                # Configura el número máximo de procesos para el procesamiento en paralelo
                maxProcesses = multiprocessing.cpu_count() - 1
                internal_maxProcs = maxProcesses
                actualCPUs = multiprocessing.cpu_count()
                overUtilized = False

                if internal_maxProcs <= 0:
                    internal_maxProcs = 1
                if internal_maxProcs > actualCPUs:
                    internal_maxProcs = actualCPUs  # No tiene sentido crear más procesos que CPUs
                    overUtilized = True

                request = "Requested [%s] processes. Reducing number of processes to be no more than the number of CPUs/Cores, which are [%s]"
                if overUtilized:
                    print(request % (maxProcesses, actualCPUs))

                futures = {}

                # Procesa los trozos de audio en paralelo
                with concurrent.futures.ThreadPoolExecutor(max_workers=internal_maxProcs) as executor:
                    for index, chunk in enumerate(chunks):
                        if index not in self.processed_chunks:
                            chunk_name = f"chunk{index}.wav"
                            temp_file = os.path.join(output_dir, chunk_name)
                            chunk.export(temp_file, format="wav")
                            # Transcribe each chunk
                            futures[index] = executor.submit(self.transcribe, temp_file, chunk_start_times[index])
                            self.processed_chunks.add(index)

                all_segments = []

                # Combina los resultados de los trozos transcritos
                for index in sorted(futures.keys()):  # Iterate over sorted chunk indices
                    future = futures[index]
                    result = future.result()
                    
                    all_segments.extend(result["segments"])

                # Ordena los segmentos según el tiempo de inicio
                all_segments.sort(key=lambda x: x["start"])

                # Convierte los segmentos en un formato de salida deseado
                output_data = [{
                    "text": segment["text"].strip(),
                    "start": segment["start"],
                    "end": segment["end"],
                    "speaker": segment["speaker"]
                } for segment in all_segments]

                print(output_data)

                self.sub.toSubtitle()

                # Remove temporary files
                for index, _ in enumerate(chunks):
                    chunk_name = f"chunk{index}.wav"
                    temp_file = os.path.join(output_dir, chunk_name)
                    os.remove(temp_file)
        except Exception as e:
            print(f"Error: {str(e)}. Reattempting transcription...")
            self.transcribe(self.audio, 0)
            self.sub.toSubtitle()

    def transcribe(self, audio_path, accumulated_time):
        try:
            self.resultado = self.whisper_model.transcribe(audio_path, word_timestamps=True)

            print("@@@@@@")
            print("@@@@@@")
            print("@@@@@@")
            print(self.resultado)
            print("@@@@@@")
            print("@@@@@@")
            print("@@@@@@")

            self.waveform, self.sample_rate = torchaudio.load(audio_path)

            # Re-muestrear el audio si la tasa de muestreo no es la deseada
            if self.sample_rate != self.SAMPLE_RATE:
                self.waveform = F.resample(self.waveform, self.sample_rate, self.SAMPLE_RATE)
                self.sample_rate = self.SAMPLE_RATE

            # Transcribir el audio a texto, incluyendo información de los tiempos de las palabras

            # Realizar la diarización de los hablantes en el audio
            self.diarization = self.diarization_pipeline(
                {"waveform": self.waveform,
                 "sample_rate": self.sample_rate},
                 min_speakers=1, max_speakers=6
            )

            # Extraer segmentos de audio con sus etiquetas de hablantes
            segments = []
            for segment, track, label in self.diarization.itertracks(yield_label=True):
                segments.append(
                    {
                        "segment": {"start": segment.start, "end": segment.end},
                        "track": track,
                        "label": label,
                    }
                )

            # Fusionar segmentos adyacentes con la misma etiqueta de hablante
            new_segments = []
            prev_segment = cur_segment = segments[0]

            for i in range(1, len(segments)):
                cur_segment = segments[i]

                if cur_segment["label"] != prev_segment["label"] and i < len(segments):
                    new_segments.append(
                        {
                            "segment": {
                                "start": prev_segment["segment"]["start"],
                                "end": cur_segment["segment"]["start"],
                            },
                            "speaker": prev_segment["label"],
                        }
                    )
                    prev_segment = segments[i]

            new_segments.append(
                {
                    "segment": {
                        "start": prev_segment["segment"]["start"],
                        "end": cur_segment["segment"]["end"],
                    },
                    "speaker": prev_segment["label"],
                }
            )

            # Asociar las palabras transcritas a los segmentos de hablantes
            final = []
            for segment in new_segments:
                start_time = segment['segment']['start']
                end_time = segment['segment']['end']
                speaker = segment['speaker']
                
                for words_info in self.resultado['segments']:
                    text = words_info["text"]
                    start = words_info["start"]
                    end = words_info["end"]

                    # Adjust timestamps of the current result
                    start += accumulated_time
                    end += accumulated_time

                    start_time += accumulated_time
                    end_time += accumulated_time
                    
                    if start_time <= start <= end_time or start_time <= end <= end_time:
                        final.append({'text': text.strip(), 'start': start, 'end': end, 'speaker': speaker})
        
            print("----------")
            print("----------")
            print("----------")
            print(final)
            print("----------")
            print("----------")
            print("----------")

            
            for dato in final:
                self.sub.toJson(dato)

            return {
                "text": self.resultado["text"],
                "segments": final,
                "accumulated_time": accumulated_time
            }
        except Exception as e:
            print(f"Error en la transcripción del archivo {audio_path}: {str(e)}")
            for seg in self.resultado['segments']:
                start = seg['start'] 
                start += accumulated_time

                end = seg['end'] 
                end += accumulated_time
                self.newSeg = {
                    'text': seg['text'],
                    'start': start,
                    'end': end,
                    'speaker': 'UNKNOW'       
                    }
                self.sub.toJson(self.newSeg)

            return {"text": self.resultado["text"], "segments": self.resultado['segments'], "accumulated_time": accumulated_time}


"""     def __init__(self, id, audio):
        self.id = id
        self.audio = audio
        self.diarization_pipeline = Pipeline.from_pretrained(
            checkpoint_path="pyannote/speaker-diarization-3.1",  # Ruta al modelo preentrenado para la diarización de hablantes
            use_auth_token='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',  # Token de autenticación para la descarga del modelo
        )
        self.transcribe_chunks()

    def transcribe_chunks(self):
        output_dir = "./tmp"
        os.makedirs(output_dir, exist_ok=True)

        audio_segment = AudioSegment.from_file(self.audio)
        silent_ranges = silence.detect_silence(audio_segment, min_silence_len=3000, silence_thresh=-40)

        chunk_start_times = [0]  # Inicialmente, el primer chunk comienza desde el inicio
        
        for silent_range in silent_ranges:
            start_time, end_time = silent_range
            # Convertir a segundos y agregar al inicio del siguiente chunk
            chunk_start_times.append(end_time / 1000)
        
        # Convertir los tiempos de inicio de los chunks en milisegundos para make_chunks
        chunk_start_times_ms = [int(time * 1000) for time in chunk_start_times]
        
        # Crear chunks basados en los tiempos de inicio calculados
        chunks = []
        for i in range(len(chunk_start_times_ms) - 1):
            chunk = audio_segment[chunk_start_times_ms[i]:chunk_start_times_ms[i + 1]]
            chunks.append(chunk)

        maxProcesses = multiprocessing.cpu_count() - 1
        internal_maxProcs = maxProcesses
        actualCPUs = multiprocessing.cpu_count()
        overUtilized = False

        if internal_maxProcs <= 0:
            internal_maxProcs = 1
        if internal_maxProcs > actualCPUs:
            internal_maxProcs = actualCPUs  # No tiene sentido crear más procesos que CPUs
            overUtilized = True

        request = "Requested [%s] processes. Reducing number of processes to be no more than the number of CPUs/Cores, which are [%s]"
        if overUtilized:
            print(request % (maxProcesses, actualCPUs))

        threads = []

        for index, chunk in enumerate(chunks):
            thread = threading.Thread(target=self.transcribe, args=(chunk, chunk_start_times[index]))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def transcribe(self, chunk, accumulated_time):
        try:
            audio_path = os.path.join("./tmp", f"{threading.current_thread().name}.wav")
            chunk.export(audio_path, format="wav")
            resultado = whisper.load_model('medium').transcribe(audio_path, fp16=False)

            print("@@@@@@")
            print("@@@@@@")
            print("@@@@@@")
            print(resultado)
            print("@@@@@@")
            print("@@@@@@")
            print("@@@@@@")

            waveform, sample_rate = torchaudio.load(audio_path)

            # Re-muestrear el audio si la tasa de muestreo no es la deseada
            if sample_rate != self.SAMPLE_RATE:
                waveform = F.resample(waveform, sample_rate, self.SAMPLE_RATE)
                sample_rate = self.SAMPLE_RATE

            # Transcribir el audio a texto, incluyendo información de los tiempos de las palabras

            # Realizar la diarización de los hablantes en el audio
            diarization = self.diarization_pipeline(
                {"waveform": waveform,
                 "sample_rate": sample_rate},
                 min_speakers=1, max_speakers=6
            )

            # Extraer segmentos de audio con sus etiquetas de hablantes
            segments = []
            for segment, track, label in diarization.itertracks(yield_label=True):
                segments.append(
                    {
                        "segment": {"start": segment.start, "end": segment.end},
                        "track": track,
                        "label": label,
                    }
                )

            # Fusionar segmentos adyacentes con la misma etiqueta de hablante
            new_segments = []
            prev_segment = cur_segment = segments[0]

            for i in range(1, len(segments)):
                cur_segment = segments[i]

                if cur_segment["label"] != prev_segment["label"] and i < len(segments):
                    new_segments.append(
                        {
                            "segment": {
                                "start": prev_segment["segment"]["start"],
                                "end": cur_segment["segment"]["start"],
                            },
                            "speaker": prev_segment["label"],
                        }
                    )
                    prev_segment = segments[i]

            new_segments.append(
                {
                    "segment": {
                        "start": prev_segment["segment"]["start"],
                        "end": cur_segment["segment"]["end"],
                    },
                    "speaker": prev_segment["label"],
                }
            )

            # Asociar las palabras transcritas a los segmentos de hablantes
            final = []
            for segment in new_segments:
                start_time = segment['segment']['start']
                end_time = segment['segment']['end']
                speaker = segment['speaker']
                
                for words_info in resultado['segments']:
                    text = words_info["text"]
                    start = words_info["start"]
                    end = words_info["end"]

                    if start_time <= start <= end_time or start_time <= end <= end_time:
                        final.append({'text': text.strip(), 'start': start, 'end': end, 'speaker': speaker})
        
            print("----------")
            print("----------")
            print("----------")
            print(final)
            print("----------")
            print("----------")
            print("----------")
            output_file = f'./tmp/{self.id}_datos.json'
            with open(output_file, 'w') as f:
                json.dump(final, f, indent=4)
                print(f"Results saved in {output_file}")
            return {
                "text": resultado["text"],
                "segments": final,
                "accumulated_time": accumulated_time
            }
        except Exception as e:
            print(f"Error en la transcripción del archivo {audio_path}: {str(e)}")
            return {"text": "", "segments": [], "accumulated_time": accumulated_time} """