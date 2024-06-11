import os
import json

def load_firebase_json():
    """Carga la configuración de Firebase desde un archivo JSON."""
    config_path = "./config/firebase.json"
    if not os.path.exists(config_path):
        raise Exception("Firebase config json not found")
    
    with open(config_path, "r") as json_file:
        firebase_config = json.load(json_file)
    
    return firebase_config

def get_mongo_connection_string():
    """Obtiene la cadena de conexión para MongoDB."""
    default_connection = "mongodb://localhost:27017/"
    container_connection = "mongodb://pcg_mongo:27017/"
    
    if os.environ.get("IS_THIS_CONTAINER", False):
        print(f"Container connection string: {container_connection}")
        return container_connection
    else:
        print(f"Local connection string: {default_connection}")
        return default_connection

'''
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
'''