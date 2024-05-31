import os # Importa el módulo os para manipulación de archivos y directorios
from processor.video_audio_split import split # Importa la función 'split' del módulo 'video_audio_split' para dividir video y audio
from processor.audio_to_text import toText # Importa la función 'toText' del módulo 'audio_to_text' para convertir audio a texto
from processor.merge import merge # Importa la función 'merge' del módulo 'merge' para fusionar archivos

class video_processor:
    def __init__(self):
        print("......Process Start......")

        # Listas de idiomas soportados (deepl)
        self.support_original_languages = ["EN", "ES", "AR", "BG", "CS", "DA", "DE", "EL", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"]
        self.support_target_languages = ["AR", "BG", "CS", "DA", "DE", "EL", "EN-GB", "EN-US", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT", "PT-BR", "PT-PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"]

    def is_supported_original(self, language):
        return language in self.support_original_languages

    def is_supported_target(self, language):
        return language in self.support_target_languages

    #objectos llegado: (self, './tmp/1234567.mp4', 'EN', 'ES')
    def process_video(self, video_path, folder_path, id, original_language, target_language):

        # Extraer el nombre del archivo sin la extensión
        self.file_name = os.path.basename(video_path)  # Obtener el nombre del archivo sin la ruta completa
       
        self.folder_path = folder_path
        print("CORE FOLDER PATH: " + self.folder_path)
        #self.file_id = os.path.splitext(self.file_name)[0]  # Quitar la extensión del archivo

        # Obtener el ID del video (parte después de la última barra y antes del punto)
        #self.id = self.file_id.split('/')[-1]  # Obtener la parte después de la última barra
        #self.id = self.id.split('.')[0]    # Obtener la parte antes del punto
        self.id = id

        self.video = video_path 
        self.original = original_language
        self.target = target_language

        try:
            if not self.video.endswith(".mp4"):
                raise ValueError("Video File Must Be .mp4 Format.")
            
            if not self.is_supported_original(self.original):
                raise ValueError("Original Language Must Be In Support List")
            
            if not self.is_supported_target(self.target):
                raise ValueError("Target Language Must Be In Support List")
            
            if self.original == self.target:
                raise ValueError("Target Language Must Be Different than Original Language")
            
            # Si todas las comprobaciones pasan

            # Verificar y procesar el archivo de audio reducido
            self.video_file_path = os.path.join(self.folder_path, f'{self.id}.mp4')
            print("CORE VIDEO FILE PATH: " + self.video_file_path)
            self.check_and_process_file(self.video_file_path, split, self.id, self.video_file_path)

            # Verificar y procesar el archivo de audio reducido
            self.audio_file_path = os.path.join(self.folder_path, f'{self.id}_audio_reduced.wav')
            print("CORE AUDIO FILE PATH: " + self.audio_file_path)
            self.check_and_process_file(self.audio_file_path, toText, self.id, self.audio_file_path, self.original, self.target)

            # Verificar y procesar el archivo de subtítulos
            self.srt_file_path = os.path.join(self.folder_path, f'{self.id}_subtitle.srt')
            print("CORE STR FILE PATH: " + self.srt_file_path)
            self.check_and_process_file(self.srt_file_path, merge, self.id, self.video_file_path, self.srt_file_path, self.target)

            print("......Process End......")

        except ValueError as error:
            # Manejo específico de la excepción ValueError
            print("Error:", error)

        except Exception as e:
            # Manejo de cualquier otra excepción que no sea ValueError
            print("Critical error!:", e)
        
        return os.path.join(self.folder_path, f'{self.id}_final.mp4')

    def check_and_process_file(self, file_path, processing_function, *args):
        """
        Verifica la existencia del archivo en la ruta especificada.
        Si el archivo existe, llama a la función de procesamiento con los argumentos dados.
        """
        if os.path.exists(file_path):
            processing_function(file_path, *args)
        else:
            print(f"The file '{file_path}' does not exist.")