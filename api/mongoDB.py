from pymongo import MongoClient

class MongoDB():
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

    def register_user(self, data): #TODO: Hash password
        print("MongoDB - register_user:\t" + str(data))
        if self.find_user_email(data["email"])  is not None:
            return False
        print("MongoDB - register_user:\t" + "No email found, proceed")
        if self.find_user_username(data["username"]) is not None:
            return False
        print("MongoDB - register_user:\t" + "No username found, proceed")

        self.users.insert_one(data)

        return True

    def update_user(self, data, email: str):
        print("MongoDB - update_user:\t" + str(data))

        operation = data["operation"]
        data.pop("operation")

        found = self.find_user_email(email)

        if found is None:
            return {"value": 404, "message": "User doesn't exist"}

        match operation:
            case "email":
                """
                if self.find_user_email(data["email"]) is not None:
                    return {"value": 400, "message": "Email already in use"}
                found["email"] = data["email"]
                """
                return {"value": 400, "message": "email not replaceable"}

            case "username":
                if self.find_user_username(data["username"])["email"] != data["email"]:
                    return {"value": 400, "message": "Username already in use"}
                found["username"] = data["username"]
                
            case "password":
                found["password"] = data["password"] #TODO: Hash password

        self.users.update_one(
            {"email": email},
            {"$set": {operation: found[operation]}}
        )

        return {"value": 0}

    def delete_user_email(self, email: str):
        found = self.find_user_email(email)
        
        if found is not None:
            self.users.delete_one({"email": found["email"]})

        return found

    def find_users(self):
        found = list(self.users.find())

        print("MongoDB - find_users:\t" + str(found))

        return found

    def find_user_email(self, email: str):
        found = self.users.find_one({"email": email})

        print("MongoDB - find_user_email:\t" + str(found))

        return found
    
    def find_user_username(self, username: str):
        found = self.users.find_one({"username": username})

        print("MongoDB - find_user_username:\t" + str(found))

        return found
    
    #* Video

    def preupload_video(self, email: str, id: str, title: str, language: str, uri: str):
        
        found = self.videos.find_one({"id": id})

        proceed = found is None

        if proceed:
            self.videos.insert_one({
                "id": id,
                "title": title,
                "language": language,
                "firebase_uri": uri,
                "video_url" : "INSERT URL" #! INSERT FIREBASE VIDEO URL AFTER PREREQUEST
                "translations": []
            })
            self.users.update_one(
                {"email": email},
                {"$push": {"videos": id} }
                )

        return proceed
    
    def insert_translation(self, id: str, sub: str, trans_id):
        found = self.videos.find_one({"id": id})
        
        if found is None:
            return False
        
        self.translated.insert_one({
            "id": trans_id,

        })

        return True
    
