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
        apikey_file = open("./config/deepl.json")
        tmp = json.load(apikey_file)
        print("apikey_file: " + tmp["key"])
        self.auth_key = tmp["key"]
        apikey_file.close()

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

        # Traduce el texto usando el método de traducción
        self.texto_traducido = self.traducir(self.datos["text"])
        # Forma un nuevo conjunto de datos con texto traducido
        self.newDatos = {
                'text': self.datos['text'],
                'texto_traducido': self.texto_traducido,
                'start': self.datos['start'],
                'end': self.datos['end'],
                'speaker': self.datos['speaker']
            }
        self.lista.append(self.newDatos)  # Agrega los datos a la lista de subtítulos
        self.lista.sort(key=lambda x: x['start'])  # Ordena los subtítulos por tiempo de inicio

        self.json_file = f'./temp/{self.id}_datos.json'  # Ruta del archivo JSON de salida
        with open(self.json_file, 'w') as f:  # Abre el archivo JSON para escritura
            json.dump(self.lista, f, indent=4)  # Escribe los datos en formato JSON
            print(f"Data appended to {self.json_file}")  # Muestra un mensaje de confirmación


    def toSubtitle(self):

        with open(self.json_file, 'r') as archivo:  # Abre el archivo JSON de subtítulos
            self.dato = json.load(archivo)  # Carga los datos JSON

        with open(f'./temp/{self.id}_subtitle.srt', 'w') as sub:  # Abre el archivo SRT de salida
            index = 1  # Inicializa el índice de subtítulo
            for i, palabra in enumerate(self.dato):  # Itera sobre los datos de subtítulos
                if i == 0:
                    start_time = palabra['start']  # Obtiene el tiempo de inicio
                end_time = palabra['end']  # Obtiene el tiempo de fin

                # Escribe el subtítulo en el archivo SRT
                sub.write(f"{index}\n{self.format_time(start_time)} --> {self.format_time(end_time)}\n{palabra['speaker']}: {palabra['texto_traducido']}\n\n")

                start_time = palabra['end']  # Actualiza el tiempo de inicio
                index += 1  # Incrementa el índice de subtítulo
            # index = 1  # Inicializa el índice de subtítulo
            # start_time = None  # Inicializa el tiempo de inicio
            # end_time = None  # Inicializa el tiempo de fin
            # subtitle = ""  # Inicializa el subtítulo
            # speaker = ""  # Inicializa el orador

            # for i, palabra in enumerate(self.dato):  # Itera sobre los datos de subtítulos
            #     word = palabra['text']  # Obtiene la palabra del subtítulo
            #     if i == 0:  # Si es la primera palabra
            #         start_time = palabra['start']  # Obtiene el tiempo de inicio
            #         subtitle += word  # Agrega la palabra al subtítulo
            #         speaker = palabra['speaker']  # Obtiene el orador
            #     else:
            #         if palabra['speaker'] != speaker or word.endswith((',', '.', '?', '!', ';', ':')):
            #             subtitle += ' ' + word  # Agrega la palabra al subtítulo
            #             end_time = palabra['end']  # Obtiene el tiempo de fin
            #             # Escribe el subtítulo en el archivo SRT
            #             sub.write(f"{index}\n{self.format_time(start_time)} --> {self.format_time(end_time)}\n{speaker + ': ' + palabra['texto_traducido']}\n\n")
            #             start_time = palabra['end']  # Actualiza el tiempo de inicio
            #             index += 1  # Incrementa el índice de subtítulo
            #             subtitle = ""  # Reinicia el subtítulo
            #             if i + 1 < len(self.dato):  # Si hay más palabras en la lista de subtítulos
            #                 speaker = self.dato[i + 1]['speaker']  # Obtiene el siguiente orador
            #         else:
            #             subtitle += ' ' + word  # Agrega la palabra al subtítulo