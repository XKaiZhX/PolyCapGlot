import json
#from googletrans import Translator
import deepl

class toSub():

    def __init__(self, id, original_language, target_language):
        self.id = id
        self.original = original_language
        self.target = target_language
        self.lista = []
        #self.toSubtitle()

    def format_time(self, seconds):

        # Convierte el tiempo en segundos a un formato de tiempo de subtítulo SRT
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def traducir(self, cadena):

        # Traduce una cadena usando DeepL API
        self.auth_key = "193d2750-9b13-45d7-be4d-44329f8e97d0:fx"
        self.textos_original = cadena
        self.target_language = 'es'
        
        # Inicializa el traductor DeepL con tu API key
        self.translator = deepl.Translator(self.auth_key)
        # Realiza la traducción de la cadena de texto
        self.textos_traducido = self.translator.translate_text(self.textos_original, source_lang=self.original, target_lang=self.target)
        
        #googletrans (free google translator api)

        #self.myTranslator = Translator()
        #self.textos_traducido = self.myTranslator.translate(self.textos_original, dest=self.target_language).text
        #return self.textos_traducido

        return self.textos_traducido.text

    def toJson(self, datos):
        self.datos = datos
        # Convierte un archivo JSON en subtítulos SRT
        # with open(self.json, 'r') as archivo:
        #     self.dato = json.load(archivo)

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

        self.json_file = f'./tmp/{self.id}_datos.json'
        with open(self.json_file, 'w') as f:
            json.dump(self.lista, f, indent=4)
            print(f"Data appended to {self.json_file}")

    def toSubtitle(self):

        with open(self.json_file, 'r') as archivo:
            self.dato = json.load(archivo)

        with open(f'./tmp/{self.id}_subtitle.srt', 'w') as sub:
            index = 1
            start_time = None
            end_time = None
            subtitle = ""
            speaker = ""

            for i, palabra in enumerate(self.dato):
                word = palabra['text']
                if i == 0:
                    start_time = palabra['start']
                    subtitle += word
                    speaker = palabra['speaker']
                else:
                    if palabra['speaker'] != speaker or word.endswith((',', '.', '?', '!', ';', ':')):
                        subtitle += ' ' + word
                        end_time = palabra['end']
                        sub.write(f"{index}\n{self.format_time(start_time)} --> {self.format_time(end_time)}\n{speaker + ': ' + palabra['texto_traducido']}\n\n")
                        start_time = palabra['end']
                        index += 1
                        subtitle = ""
                        if i + 1 < len(self.dato):
                            speaker = self.dato[i + 1]['speaker']
                    else:
                        subtitle += ' ' + word