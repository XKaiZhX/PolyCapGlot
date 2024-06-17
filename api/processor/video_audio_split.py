from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from scipy.io import wavfile
from noisereduce import reduce_noise
import numpy as np

class split():

    def __init__(self, path, id, video):
        self.id = id
        self.video = video
        self.path = path
        self.separar()

    def separar(self):
        try:
            print("......Separating video and audio......")
            # Cargar video
            video_editor = VideoFileClip(self.video)
            # Separar parte audio
            audio_editor = video_editor.audio
            # Guardar parte audio como fichero
            audio_editor.write_audiofile(f'{self.path}/{self.id}_audio.wav')
            # Cerrar recursos
            video_editor.close()
            audio_editor.close()
            # Reducir ruido
            self.reducir_ruido()
        except Exception as e:
            print("Error occurred during audio splitting:", str(e))

    def reducir_ruido(self):
        try:
            print("......Reducing noise......")
            # Cargar los datos de audio del archivo guardado
            rate, data = wavfile.read(f'{self.path}/{self.id}_audio.wav')
            orig_shape = data.shape
            data = np.reshape(data, (2, -1))
            # Realizar reducción de ruido
            reduced_noise = reduce_noise(
                y=data,
                sr=rate,
                stationary=True
            )
            # Escribir los datos de audio reducidos de ruido en un nuevo archivo
            wavfile.write(f'{self.path}/{self.id}_audio_reduced.wav', rate, reduced_noise.reshape(orig_shape))
        except Exception as e:
            print("Error occurred during noise reduction:", str(e))
