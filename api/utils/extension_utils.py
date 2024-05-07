from moviepy.config import change_settings
import os
import json

def load_firebase_json():
    firebase_config = None
    if os.path.exists("./config/firebase.json"):
        json_file = open("./config/firebase.json")
        firebase_config = json.load(json_file)
        json_file.close()
        
    if firebase_config is None:
        raise Exception("Firebase config json not found")

    return firebase_config

def get_mongo_connection_string():
    connection = "mongodb://localhost:27017/"
    key = os.environ.get("IS_THIS_CONTAINER", False)
    if key:
        connection = "mongodb://pcg_mongo:27017/"
        print("Container connection string: " + connection)
    else:
        print("Local connection string: " + connection)
    
    return connection

def configure_moviepy():
    key = os.environ.get("IS_THIS_CONTAINER", False)
    if key:
        print("ImageMagik updated")
        change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert-im6.q16"})