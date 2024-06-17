import os # Importa el módulo os para manipulación de archivos y directorios
from processor.video_audio_split import split # Importa la función 'split' del módulo 'video_audio_split' para dividir video y audio
from processor.audio_to_text import toText # Importa la función 'toText' del módulo 'audio_to_text' para convertir audio a texto
from processor.merge import merge # Importa la función 'merge' del módulo 'merge' para fusionar archivos

SUPPORTED_ORIGINAL_LANGUAGES = ["EN", "ES", "AR", "BG", "CS", "DA", "DE", "EL", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"]
SUPPORTED_TARGET_LANGUAGES = ["AR", "BG", "CS", "DA", "DE", "EL", "EN-GB", "EN-US", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT", "PT-BR", "PT-PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"]

class video_processor:
    def __init__(self):
        print("......Process Start......")

    def is_supported_original(self, language):
        return language in SUPPORTED_ORIGINAL_LANGUAGES

    def is_supported_target(self, language):
        return language in SUPPORTED_TARGET_LANGUAGES

    def process_video(self, video_path, folder_path, id, original_language, target_language):
        try:
            file_name = os.path.basename(video_path)
            video_file_path = os.path.join(folder_path, f'{id}.mp4')

            if not video_path.endswith(".mp4"):
                raise ValueError("Video File Must Be .mp4 Format.")
            if not self.is_supported_original(original_language):
                raise ValueError("Original Language Must Be In Support List")
            if not self.is_supported_target(target_language):
                raise ValueError("Target Language Must Be In Support List")
            if original_language == target_language:
                raise ValueError("Target Language Must Be Different than Original Language")

            # Verificar y procesar el archivo de audio reducido
            video_file_path = os.path.join(folder_path, f'{id}.mp4')
            self.check_and_process_file(video_file_path, split, folder_path, id, video_file_path)

            # Verificar y procesar el archivo de audio reducido
            audio_file_path = os.path.join(folder_path, f'{id}_audio_reduced.wav')
            self.check_and_process_file(audio_file_path, toText, folder_path, id, audio_file_path, original_language, target_language)

            # Verificar y procesar el archivo de subtítulos
            srt_file_path = os.path.join(folder_path, f'{id}_subtitle.srt')
            self.check_and_process_file(srt_file_path, merge, folder_path, id, video_file_path, srt_file_path, target_language)

            print("......Process End......")
            
            return os.path.join(folder_path, f'{id}_final.mp4')
        except ValueError as error:
            print("Error:", error)
        except Exception as e:
            print("Critical error!:", e)

    def check_and_process_file(self, file_path, process_class, *args):
        if os.path.exists(file_path):
            print("Ejecutando: " + processing_function.__name__)
            processing_function(*args)
        else:
            print(f"The file '{file_path}' does not exist.")
