from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from scipy.io import wavfile
import noisereduce as nr
import numpy as np

class split():

    def __init__(self, id, video):
        self.id = id
        self.video = video

        self.separar()

    def separar(self): 

        try:
            print("......Separating video and audio......")

            #cargar video
            self.video_editor = VideoFileClip(self.video)

            #separar parte audio
            self.audio_editor = self.video_editor.audio

            #Guardar parte audio como fichero
            #Puede ser de formato wav tambien 'audio.wav', si quiere ser de formato mp3, './files/audio.mp3', codec='mp3'
            self.audio_editor.write_audiofile(f'./tmp/{self.id}_audio.wav')
            
            #Cerrar proceso
            self.video_editor.close()
            self.audio_editor.close()

            self.reducir_ruido()
        except Exception as e:
            print("Error occurred during audio splitting:", str(e))

    def reducir_ruido(self):

        try:
            #Cargar los datos de audio del archivo guardado
            self.rate, self.data = wavfile.read(f'./tmp/{self.id}_audio.wav')
            self.orig_shape = self.data.shape
            self.data = np.reshape(self.data, (2, -1))

            # Realizar reducción de ruido (optimizado para voz)
            self.reduced_noise = nr.reduce_noise(
                y=self.data, # Array de datos de audio
                sr=self.rate, # Tasa de muestreo de los datos de audio
                stationary=True # Si se asume que el ruido es estacionario (constante) o no
            )

            # Escribir los datos de audio reducidos de ruido en un nuevo archivo
            wavfile.write(f'./tmp/{self.id}_audio_reduced.wav', self.rate, self.reduced_noise.reshape(self.orig_shape))
        except Exception as e:
            print("Error occurred during audio reducing:", str(e))