#from extensions import storage, firebase
#storage.delete("videoTest", None)

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