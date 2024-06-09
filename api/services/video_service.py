from abc import abstractmethod 
from abc import ABCMeta

from extensions import db

class AbstractVideoService(metaclass=ABCMeta):
    @abstractmethod
    def preupload_video(self, email: str, id: str, title: str, language: str, uri: str):
        pass

    def find_video(self, id: str):
        pass

    def get_user_videos(self, videos):
        pass

    def delete_video(self, id: str, email: str):
        pass

    def delete_trans(self, id: str, email: str):
        pass

class VideoService(AbstractVideoService):
    def preupload_video(self, email: str, id: str, title: str, language: str, uri: str):
        return db.preupload_video(email, id, title, language, uri)
    
    def find_video(self, id: str):
        return db.find_video(id)
    
    def insert_translation(self, id: str, sub: str, trans_id):
        return db.insert_translation(id, sub, trans_id)

    def delete_video(self, id: str, email: str):
        return db.delete_video(self, id, email)

    def delete_trans(self, trans_id: str, video_id: str):
        return db.delete_translation(self, trans_id, video_id)

    def get_user_videos(self, videos):
        list = []
        for video_id in videos:
            video = self.find_video(video_id)
            list.append({
                "title": video["title"],
                "language": video["language"],
                "firebase_uri": video["firebase_uri"],
                "translations" : db.get_translations(video["id"])
            })
        return list