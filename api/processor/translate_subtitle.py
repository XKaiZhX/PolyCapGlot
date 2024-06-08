import json
import os
import deepl

class toSub:
    def __init__(self, id, original_language, target_language):
        self.id = id
        self.original = original_language
        self.target = target_language
        self.lista = []

    def format_time(self, seconds):
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = int(seconds % 60)
            milliseconds = int((seconds - int(seconds)) * 1000)
            return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
        except Exception as e:
            print("Error:", e)

    def traducir(self, cadena):
        try:
            # Carga la clave de autenticación desde el archivo de configuración
            with open("./config/deepl.json") as apikey_file:
                tmp = json.load(apikey_file)
                print("apikey_file: " + tmp["key"])
                self.auth_key = tmp["key"]

            # Traduce el texto utilizando la API de DeepL
            self.textos_original = cadena
            self.translator = deepl.Translator(self.auth_key)
            self.textos_traducido = self.translator.translate_text(
                self.textos_original, source_lang=self.original, target_lang=self.target
            )
            return self.textos_traducido.text
        except Exception as e:
            print("Error:", e)

    def toJson(self, datos):
        try:
            # Traduce el texto y lo agrega a la lista de datos
            self.datos = datos
            self.texto_traducido = self.traducir(self.datos["text"])

            self.newDatos = {
                'text': self.datos['text'],
                'texto_traducido': self.texto_traducido,
                'start': self.datos['start'],
                'end': self.datos['end'],
                'speaker': self.datos['speaker']
            }

            self.lista.append(self.newDatos)
            self.lista.sort(key=lambda x: x['start'])

            # Guarda la lista de datos en un archivo JSON
            self.json_file = f'./tmp/{self.id}_{self.original}_{self.target}/{self.id}_datos.json'
            os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
            with open(self.json_file, 'w') as f:
                json.dump(self.lista, f, indent=4)
                print(f"Data appended to {self.json_file}")
        except Exception as e:
            print("Error:", e)

    def toSubtitle(self):
        try:
            # Carga los datos del archivo JSON
            with open(self.json_file, 'r') as archivo:
                self.dato = json.load(archivo)

            # Crea un archivo de subtítulos en formato SRT
            srt_file = f'./tmp/{self.id}_{self.original}_{self.target}/{self.id}_subtitle.srt'
            with open(srt_file, 'w') as sub:
                index = 1
                for i, palabra in enumerate(self.dato):
                    if i == 0:
                        start_time = palabra['start']
                    end_time = palabra['end']

                    # Escribe cada subtítulo en el archivo SRT
                    sub.write(f"{index}\n{self.format_time(start_time)} --> {self.format_time(end_time)}\n{palabra['speaker']}: {palabra['texto_traducido']}\n\n")

                    start_time = palabra['end']
                    index += 1
            print(f"Subtitles written to {srt_file}")
        except Exception as e:
            print("Error:", e)
