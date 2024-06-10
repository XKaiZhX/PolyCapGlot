from pymongo import MongoClient
import time

from utils.firebase_utils import delete_file

class MongoRepository():
    def __init__(self, host):
        print("Intentando conectarse a MongoDB en", host)
        self.client = MongoClient(host)

        self.bbdd = self.client["test_polycapglot"]

        self.users = self.bbdd["users"]
        self.videos = self.bbdd["videos"]
        self.translated = self.bbdd["translated"]

    #* User

    def insert_user(self, username, email, password, salt):
        self.users.insert_one({
            "username": username,
            "email": email,
            "password": password,
            "salt": salt,
            "videos": []
        })
        
    def update_user_username(self, email, username):
        return self.users.update_one(
            {"email": email},
            {"$set": {"username": username}}
        ).matched_count == 1;

    def update_user_password(self, email, password):
        return self.users.update_one(
            {"email": email},
            {"$set": {"password": password}}
        ).matched_count == 1;

    def find_users(self):
        return list(self.users.find())

    def find_user(self, email: str):
        return self.users.find_one({"email": email})
    
    def find_by_username(self, username: str):
        found = list()
        
        for user in self.users.find({"username": username}):
            found.append(user)

        return found
    
    def delete_user(self, email:str):
        user_found = self.find_user(email)
        if user_found is None:
            return False
        
        for video_id in user_found["videos"]:
            result = self.delete_video(video_id, email)
            if result == False:
                return False
        
        self.users.delete_one({"email": email})

        return True
    #* Video

    def delete_video(self, id, email):
        found = self.find_video(id)
        if found is None:
            return False
        
        for translation_id in found["translations"]:
            result = self.delete_translation(translation_id, found["id"])
            if result == False:
                return False
        
        delete_file(found["firebase_uri"])
        result = self.videos.delete_one({"id": id})

        if result.deleted_count > 0:
            self.users.update_one(
                {"email": email},
                {"$pull": {"videos": id}}
            )
            return True

        return False

    def find_video(self, id):
        return self.videos.find_one({"id": id})

    def preupload_video(self, email: str, id: str, title: str, language: str, uri: str):
        
        found = self.videos.find_one({"id": id})

        proceed = found is None

        if proceed:
            insert = {
                "id": id,
                "title": title,
                "language": language,
                "firebase_uri": uri,
                "translations": []
            }
            self.videos.insert_one(insert)
            self.users.update_one(
                {"email": email},
                {"$push": {"videos": id} }
                )
            return insert

        return proceed
    
    def insert_translation(self, id: str, sub: str, trans_id):
        print("MongoRepository - insert_translation:\t" + f"id={id}, sub={sub}, trans_id={trans_id}")
        found = self.videos.find_one({"id": id})
        print("found" + str(found))

        if found is None:
            return False

        uri = f"translated_videos/{trans_id}.mp4"

        self.translated.insert_one({
            "id": trans_id,
            "sub_language": sub,
            "firebase_uri": uri,
            "status": 0
        })

        print

        self.videos.find_one_and_update(
            {"id": found["id"]},
            {"$push": {"translations": trans_id}}
        )

        return True
    
# translations
    def find_translation(self, trans_id: str):
        return self.translated.find_one({"id": trans_id})
    
    def get_translations(self, video_id: str):
        #print("MongoRepository - insert_translation:\t" + f"video_id={video_id}")

        found = self.find_video(video_id)

        trans_list = []
        for trans_id in found["translations"]:
            trans_found = self.find_translation(trans_id)
            trans_list.append({
                "id": trans_found["id"],
                "sub_language": trans_found["sub_language"],
                "firebase_uri": trans_found["firebase_uri"],
                "status": trans_found["status"]
            })

        return trans_list
    
    def delete_translation(self, id, video_id):
        found = self.find_translation(id)

        if found is None:
            return False
        
        if found["status"] == 0:
            return False
        
        if found["status"] == 1:
            delete_file(found["firebase_uri"])

        result = self.translated.delete_one({"id": id})

        if result.deleted_count > 0:
            self.videos.update_one(
                {"id": video_id},
                {"$pull": {"translations": id}}
            )
            return True

        return False