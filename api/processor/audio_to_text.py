import json  # Importa el módulo json para manejar datos JSON
from pyannote.audio import Pipeline  # Importa la clase Pipeline del módulo pyannote.audio para el procesamiento de audio
from pydub import AudioSegment  # Importa la clase AudioSegment del módulo pydub para manipulación de audio
from pydub.utils import make_chunks  # Importa la función make_chunks del módulo pydub.utils para dividir audio en trozos
import concurrent.futures  # Importa el módulo concurrent.futures para realizar cómputo en paralelo
import whisper  # Importa el módulo whisper para transcribir audio
import os  # Importa el módulo os para manipulación de archivos y directorios
from time import perf_counter  # Importa la función perf_counter del módulo time para medir el tiempo de ejecución
import torchaudio  # Importa el módulo torchaudio para procesamiento de audio con PyTorch
from torchaudio import functional as F  # Importa el módulo functional de torchaudio para funciones de procesamiento de audio
from pydub.silence import split_on_silence  # Importa la función split_on_silence del módulo pydub.silence para dividir audio en silencios
import pydub.silence as silence  # Importa el módulo silence de pydub para detección de silencio
import multiprocessing  # Importa el módulo multiprocessing para realizar procesamiento en paralelo
from processor.translate_subtitle import toSub  # Importa la clase toSub del módulo translate_subtitle para traducir subtítulos
import threading  # Importa el módulo threading para crear y gestionar subprocesos

class toText:
    SAMPLE_RATE = 16000

    def __init__(self, path, id, audio, original_language, target_language):
        self.completed = False
        self.path = path
        self.id = id
        self.audio = audio
        self.original = original_language
        self.target = target_language

        self.diarization_pipeline = Pipeline.from_pretrained(
            checkpoint_path="pyannote/speaker-diarization-3.1",
            use_auth_token='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'
        )

        self.sub = toSub(self.id, self.original, self.target)
        self.whisper_model = whisper.load_model('medium')
        self.processed_chunks = set()

        self.transcribe_chunks()

    def transcribe_chunks(self):
        try:
            output_dir = self.path
            os.makedirs(output_dir, exist_ok=True)

            audio_segment = AudioSegment.from_file(self.audio)
            audio_duration = len(audio_segment) / 1000

            if audio_duration < 60:
                print("Audio is too short.")
                self.transcribe(self.audio, 0)
                self.sub.toSubtitle()
            else:
                min_silence_len = 5000  # Longitud inicial del silencio en milisegundos

                while min_silence_len >= 0:  # Intenta con diferentes longitudes mínimas de silencio

                    silent_ranges = silence.detect_silence(audio_segment, min_silence_len=min_silence_len, silence_thresh=-40)

                    if silent_ranges:  # Si se detectan silencios, procede con el proceso
                        break

                    min_silence_len -= 500  # Disminuye la longitud mínima del silencio en 1 segundo

                if not silent_ranges:  # Si no se detectan silencios
                    print("No silence detected in the audio.")
                    self.transcribe(self.audio, 0)  # Transcribe el audio completo
                    self.sub.toSubtitle()  # Traduce los subtítulos
                else:
                    chunk_start_times = [0]
                    
                    for silent_range in silent_ranges:
                        _, end_time = silent_range
                        chunk_start_times.append(end_time / 1000)
                    
                    chunk_start_times.append(audio_duration)

                    print(chunk_start_times)
                
                    chunk_start_times_ms = [int(time * 1000) for time in chunk_start_times]
                    chunks = []
                    for i in range(len(chunk_start_times_ms) - 1):
                        chunk = audio_segment[chunk_start_times_ms[i]:chunk_start_times_ms[i + 1]]
                        chunks.append(chunk)

                    if not chunks:
                        raise ValueError("La lista 'chunks' está vacía. No se generaron trozos de audio.")

                    max_processes = max(1, min(multiprocessing.cpu_count() - 1, len(chunks)))
                    print(f"Utilizing {max_processes} parallel processes.")

                    futures = {}
                    with concurrent.futures.ThreadPoolExecutor(max_workers=max_processes) as executor:
                        for index, chunk in enumerate(chunks):
                            if index not in self.processed_chunks:
                                chunk_name = f"chunk{index}.wav"
                                temp_file = os.path.join(output_dir, chunk_name)
                                chunk.export(temp_file, format="wav")

                                futures[index] = executor.submit(self.transcribe, temp_file, chunk_start_times[index])

                                self.processed_chunks.add(index)

                    all_segments = []
                    for index in sorted(futures.keys()):
                        print(index)
                        future = futures[index]
                        result = future.result()
                        all_segments.extend(result["segments"])
                        print(result["segments"])

                    all_segments.sort(key=lambda x: x["start"])
                    output_data = [{
                        "text": segment["text"].strip(),
                        "start": segment["start"],
                        "end": segment["end"],
                        "speaker": segment["speaker"]
                    } for segment in all_segments]

                    print(output_data)
                    self.sub.toSubtitle()

                    for index in range(len(chunks)):
                        chunk_name = f"chunk{index}.wav"
                        temp_file = os.path.join(output_dir, chunk_name)
                        os.remove(temp_file)

                    self.completed = True
        except Exception as e:
            print(f"Error: {str(e)}. Reattempting transcription...")
            self.transcribe(self.audio, 0)
            self.completed = self.sub.toSubtitle()

        return self.completed

    def transcribe(self, audio_path, accumulated_time):
        try:
            self.whisper_model_chunk = whisper.load_model('medium')
            resultado = self.whisper_model_chunk.transcribe(audio_path, language=self.original, word_timestamps=True)
            waveform, sample_rate = torchaudio.load(audio_path)

            if sample_rate != self.SAMPLE_RATE:
                waveform = F.resample(waveform, sample_rate, self.SAMPLE_RATE)
                sample_rate = self.SAMPLE_RATE

            diarization = self.diarization_pipeline(
                {"waveform": waveform, "sample_rate": sample_rate},
                min_speakers=1, max_speakers=6
            )

            segments = []
            for segment, _, label in diarization.itertracks(yield_label=True):
                segments.append({"segment": {"start": segment.start, "end": segment.end}, "speaker": label})

            new_segments = []
            prev_segment = segments[0]

            for cur_segment in segments[1:]:
                if cur_segment["speaker"] != prev_segment["speaker"]:
                    new_segments.append({
                        "segment": {"start": prev_segment["segment"]["start"], "end": cur_segment["segment"]["start"]},
                        "speaker": prev_segment["speaker"]
                    })
                    prev_segment = cur_segment

            new_segments.append({
                "segment": {"start": prev_segment["segment"]["start"], "end": cur_segment["segment"]["end"]},
                "speaker": prev_segment["speaker"]
            })

            final = []
            for segment in new_segments:
                start_time = segment['segment']['start']
                end_time = segment['segment']['end']
                speaker = segment['speaker']

                for words_info in resultado['segments']:
                    text = words_info["text"]
                    start = words_info["start"]
                    end = words_info["end"]
                    
                    print(start_time)
                    print(start)
                    print(end_time)
                    print(end)

                    if start_time <= start <= end_time or start_time <= end <= end_time:
                        start += accumulated_time
                        end += accumulated_time
                        final.append({'text': text.strip(), 'start': start, 'end': end, 'speaker': speaker})

            for dato in final:
                self.sub.toJson(dato)

            return {
                "text": resultado["text"],
                "segments": final,
                "accumulated_time": accumulated_time
            }
        
        except Exception as e:
            print(f"Error en la transcripción del archivo {audio_path}: {str(e)}")
            resultado = {"segments": []}
            for seg in resultado['segments']:
                start = seg['start'] + accumulated_time
                end = seg['end'] + accumulated_time
                self.sub.toJson({'text': seg['text'], 'start': start, 'end': end, 'speaker': 'UNKNOW'})
            self.completed = False

            return {"text": resultado.get("text", ""), "segments": resultado['segments'], "accumulated_time": accumulated_time}
            

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
