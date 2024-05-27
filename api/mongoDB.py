from pymongo import MongoClient
import time
class MongoRepository():
    def __init__(self, host):
        print("Intentando conectarse a MongoDB en", host)
        self.client = MongoClient(host)

        self.bbdd = self.client["test_polycapglot"]

        self.users = self.bbdd["users"]
        self.videos = self.bbdd["videos"]
        self.translated = self.bbdd["translated"]
        self.counters = self.bbdd["counters"]

        self.initialize_counters()
    
    def initialize_counters(self):
        ''' No hace falta un id de usuario, se usa EMAIL
        u_counter = self.counters.find_one({"_id": "user_counter"})
        if u_counter is None:
            self.counters.insert_one({
                "_id": "user_counter",
                "value": 0
                })
        else:
            print("MongoDB:\tuser_counter found starting by ", u_counter["value"])
        '''

        v_counter = self.counters.find_one({"_id": "video_counter"})
        if v_counter is None:
            self.counters.insert_one({
                "_id": "video_counter",
                "value": 0
                })
        else:
            print("MongoDB:\tvideo_counter found starting by ", v_counter["value"])
    
    '''
    def next_user_id(self):
        counter = self.counters.find_one_and_update(
            {"_id": "user_counter"},
            {"$inc" : { "value" : 1 }}
        )
        return counter["value"]
    '''

    def next_video_id(self):
        counter = self.counters.find_one_and_update(
            {"_id": "video_counter"},
            {"$inc" : { "value" : 1 }}
        )
        return counter["value"]

    #* User

    def insert_user(self, username, email, password, salt):
        self.users.insert_one({
            "username": username,
            "email": email,
            "password": password,
            "salt": salt
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

    def delete_user(self, email: str):
        found = self.users.find_one_and_delete({"email": email})

        return found

    def find_users(self):
        return list(self.users.find())

    def find_user(self, email: str):
        return self.users.find_one({"email": email})
    
    def find_by_username(self, username: str):
        found = list()
        
        for user in self.users.find({"username": username}):
            found.append(user)

        return found
    
    #* Video

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
        print("MongoRepository - insert_translation:\t" + f"video_id={video_id}")

        found = self.find_video(video_id)

        trans_list = []
        for trans_id in found["translations"]:
            trans_found = self.find_translation(trans_id)
            trans_list.append({
                "sub_language": trans_found["sub_language"],
                "firebase_uri": trans_found["firebase_uri"]
            })

        return trans_list