import json
import os
import deepl

class toSub:
    def __init__(self, id, original_language, target_language):
        """
        Clase para manejar la creación y traducción de subtítulos.

        :param id: Identificador único para el archivo de subtítulos.
        :param original_language: Código del idioma original (ej. 'EN').
        :param target_language: Código del idioma objetivo para la traducción (ej. 'ES').
        """
        self.id = id
        self.original = original_language
        self.target = target_language
        self.lista = []
        self.json_file = ''
        self.auth_key = self.load_api_key()
        self.translator = deepl.Translator(self.auth_key)

    def load_api_key(self):
        """
        Carga la clave de API de DeepL desde el archivo de configuración.

        :return: Clave de API de DeepL.
        """
        try:
            with open("./config/deepl.json") as apikey_file:
                return json.load(apikey_file)["key"]
        except Exception as e:
            print(f"Error al cargar la clave de API: {e}")
            raise

    def format_time(self, seconds):
        """
        Formatea el tiempo en segundos a formato SRT.

        :param seconds: Tiempo en segundos.
        :return: Tiempo formateado en formato SRT.
        """
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = int(seconds % 60)
            milliseconds = int((seconds - int(seconds)) * 1000)
            return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
        except Exception as e:
            print(f"Error al formatear el tiempo: {e}")
            return "00:00:00,000"

    def traducir(self, cadena):
        """
        Traduce una cadena de texto usando la API de DeepL.

        :param cadena: Texto a traducir.
        :return: Texto traducido.
        """
        try:
            return self.translator.translate_text(cadena, source_lang=self.original, target_lang=self.target).text
        except Exception as e:
            print(f"Error en la traducción: {e}")
            return cadena

    def toJson(self, datos):
        """
        Convierte los datos en formato JSON y los guarda en un archivo.

        :param datos: Datos a convertir y guardar.
        """
        try:
            self.texto_traducido = self.traducir(datos["text"])

            new_datos = {
                'text': datos['text'],
                'texto_traducido': self.texto_traducido,
                'start': datos['start'],
                'end': datos['end'],
                'speaker': datos['speaker']
            }

            self.lista.append(new_datos)
            self.lista.sort(key=lambda x: x['start'])

            self.json_file = f'./tmp/{self.id}_{self.original}_{self.target}/{self.id}_datos.json'
            os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
            with open(self.json_file, 'w') as f:
                json.dump(self.lista, f, indent=4)
                print(f"Data appended to {self.json_file}")
        except Exception as e:
            print(f"Error al convertir a JSON: {e}")

    def toSubtitle(self):
        """
        Crea un archivo de subtítulos en formato SRT a partir de los datos JSON.
        """
        try:
            if not self.json_file:
                print("Error: No json_file available")
                return

            with open(self.json_file, 'r') as archivo:
                datos = json.load(archivo)

            srt_file = f'./tmp/{self.id}_{self.original}_{self.target}/{self.id}_subtitle.srt'
            os.makedirs(os.path.dirname(srt_file), exist_ok=True)
            with open(srt_file, 'w') as sub:
                for index, palabra in enumerate(datos, start=1):
                    start_time = palabra['start']
                    end_time = palabra['end']
                    sub.write(f"{index}\n{self.format_time(start_time)} --> {self.format_time(end_time)}\n{palabra['speaker']}: {palabra['texto_traducido']}\n\n")
            print(f"Subtitles written to {srt_file}")
        except Exception as e:
            print(f"Error al crear el archivo de subtítulos: {e}")
