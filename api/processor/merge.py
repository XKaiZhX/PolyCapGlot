import os
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class merge():
    def __init__(self, path, id, video, subtitulo, target_language):
        self.completed = False
        self.path = path
        self.id = id
        self.video = video
        self.subtitulo = subtitulo
        self.target = target_language

        self.juntar()

    def set_encoding(self, target):
        language_encoding = 'utf-8'
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

    def juntar(self):
        try:
            self.video_editor = VideoFileClip(self.video)
            self.language_code = self.set_encoding(self.target)
            self.srt_editor = pysrt.open(self.subtitulo, encoding=self.language_code)
            self.subtitulos = self.create_subtitle_clips(self.srt_editor, self.video_editor.size)
            self.final_video = CompositeVideoClip([self.video_editor] + self.subtitulos)
            self.output_file = os.path.join(f'{self.path}/{self.id}_final.mp4')
            self.final_video.write_videofile(self.output_file)
            self.completed = True
        except Exception as e:
            print("Error al juntar el video con los subtítulos:", e)
            self.completed = False

    def time_to_seconds(self, time_obj):
        return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

    def create_subtitle_clips(self, subtitles, videosize, fontsize=24, font='Arial', color='yellow'):
        self.subtitle_clips = []
        for subtitle in subtitles:
            self.start_time = self.time_to_seconds(subtitle.start)
            self.end_time = self.time_to_seconds(subtitle.end)
            self.duration = self.end_time - self.start_time
            self.video_width, self.video_height = videosize

            text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color='black',
                                 size=(self.video_width * 3 / 4, None), method='caption').set_start(self.start_time).set_duration(self.duration)

            subtitle_x_position = 'center'
            subtitle_y_position = self.video_height * 4 / 5
            text_position = (subtitle_x_position, subtitle_y_position)

            self.subtitle_clips.append(text_clip.set_position(text_position))
        return self.subtitle_clips
