import firebase_admin
from firebase_admin import credentials, storage
from utils.extension_utils import load_firebase_json

# Inicializar Firebase Admin SDK
def initialize_firebase_admin():
    """Inicializa Firebase Admin SDK con credenciales y configuración."""
    cred_path = "./config/firebase_service.json"
    firebase_config = load_firebase_json()
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': firebase_config["storageBucket"]
    })

# Función para eliminar un archivo
def delete_file(file_path):
    """Elimina un archivo de Firebase Storage."""
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_path)
        blob.delete()
        print(f"File {file_path} deleted successfully.")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

# Inicializa Firebase Admin al importar el módulo
initialize_firebase_admin()

'''
import firebase_admin
from utils.extension_utils import load_firebase_json
from firebase_admin import credentials, storage

# Initialize Firebase Admin SDK
cred = credentials.Certificate("./config/firebase_service.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': load_firebase_json()["storageBucket"]
})

# Function to delete a file
def delete_file(file_path):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_path)
        blob.delete()
        print(f"File {file_path} deleted successfully.")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
'''