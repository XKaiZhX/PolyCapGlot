from abc import abstractmethod 
from abc import ABCMeta

from extensions import db

class AbstractVideoService(metaclass=ABCMeta):
    @abstractmethod
    def preupload_video(self, email: str, id: str, title: str, language: str, uri: str):
        pass

    def find_video(self, id: str):
        pass

class VideoService(AbstractVideoService):
    def preupload_video(self, email: str, id: str, title: str, language: str, uri: str):
        return db.preupload_video(email, id, title, language, uri)
    
    def find_video(self, id: str):
        return db.find_video(id)