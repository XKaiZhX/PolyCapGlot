import os
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class merge():
    def __init__(self, path, id, video, subtitulo, target_language):
        """
        Clase para fusionar un video con subtítulos.

        :param path: Ruta de salida para el archivo de video fusionado.
        :param id: Identificador único para el archivo de video.
        :param video: Ruta del archivo de video original.
        :param subtitulo: Ruta del archivo de subtítulos (SRT).
        :param target_language: Código del idioma objetivo para la codificación de subtítulos.
        """
        self.completed = False
        self.path = path
        self.id = id
        self.video = video
        self.subtitulo = subtitulo
        self.target = target_language

        self.merge_video_with_subtitles()

    def set_encoding(self, target):
        """
        Configura la codificación del archivo de subtítulos según el idioma objetivo.

        :param target: Código del idioma objetivo.
        :return: Codificación correspondiente.
        """
        encoding_map = {
            'ZH': 'hzgb',
            'AR': 'cp720',
            'BG': 'cp1251',
            'CS': 'iso8859_2',
            'DA': 'iso8859_1',
            'DE': 'iso8859_1',
            'EL': 'iso8859_7',
            'EN': 'iso8859_1',
            'EN-GB': 'iso8859_1',
            'EN-US': 'iso8859_1',
            'ES': 'iso8859_1',
            'ET': 'iso8859_4',
            'FI': 'iso8859_1',
            'FR': 'iso8859_1',
            'HU': 'iso8859_2',
            'ID': 'iso8859_1',
            'IT': 'iso8859_1',
            'JA': 'cp932',
            'KO': 'cp949',
            'LT': 'iso8859_13',
            'LV': 'iso8859_4',
            'NB': 'iso8859_1',
            'NL': 'iso8859_1',
            'PL': 'iso8859_2',
            'PT': 'iso8859_1',
            'PT-BR': 'iso8859_1',
            'PT-PT': 'iso8859_1',
            'RO': 'iso8859_2',
            'RU': 'cp1251',
            'SK': 'iso8859_2',
            'SL': 'iso8859_2',
            'SV': 'iso8859_1',
            'TR': 'iso8859_9',
            'UK': 'cp1251',
        }
        return encoding_map.get(target, 'utf-8')

    def merge_video_with_subtitles(self):
        """
        Fusiona el video con los subtítulos y guarda el archivo resultante.
        """
        try:
            video_clip = VideoFileClip(self.video)
            encoding = self.set_encoding(self.target)
            subtitles = pysrt.open(self.subtitulo, encoding=encoding)
            subtitle_clips = self.create_subtitle_clips(subtitles, video_clip.size)
            final_video = CompositeVideoClip([video_clip] + subtitle_clips)
            output_file = os.path.join(self.path, f'{self.id}_final.mp4')
            os.makedirs(self.path, exist_ok=True)
            final_video.write_videofile(output_file)
            self.completed = True
        except Exception as e:
            print(f"Error al juntar el video con los subtítulos: {e}")
            self.completed = False

    def time_to_seconds(self, time_obj):
        """
        Convierte un objeto de tiempo en segundos.

        :param time_obj: Objeto de tiempo (pysrt.SubRipTime).
        :return: Tiempo en segundos.
        """
        return (time_obj.hours * 3600 + time_obj.minutes * 60 +
                time_obj.seconds + time_obj.milliseconds / 1000)

    def create_subtitle_clips(self, subtitles, videosize, fontsize=24, font='Arial', color='yellow'):
        """
        Crea clips de subtítulos para superponer en el video.

        :param subtitles: Lista de subtítulos (pysrt.SubRipFile).
        :param videosize: Tamaño del video (ancho, alto).
        :param fontsize: Tamaño de la fuente de los subtítulos.
        :param font: Nombre de la fuente de los subtítulos.
        :param color: Color de la fuente de los subtítulos.
        :return: Lista de clips de subtítulos (moviepy.editor.TextClip).
        """
        subtitle_clips = []
        video_width, video_height = videosize

        for subtitle in subtitles:
            start_time = self.time_to_seconds(subtitle.start)
            end_time = self.time_to_seconds(subtitle.end)
            duration = end_time - start_time

            text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color='black',
                                 size=(video_width * 3 / 4, None), method='caption').set_start(start_time).set_duration(duration)

            text_clip = text_clip.set_position(('center', video_height * 4 / 5))
            subtitle_clips.append(text_clip)
        
        return subtitle_clips
