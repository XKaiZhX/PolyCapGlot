from mongoDB import MongoRepository
from flask_restx import Api
from processor.core import video_processor
from utils.extension_utils import get_mongo_connection_string, load_firebase_json
import pyrebase

# Inicializa la conexión a la base de datos MongoDB
def initialize_db():
    connection_string = get_mongo_connection_string()
    return MongoRepository(connection_string)

# Configura y devuelve la instancia de la API de Flask-RESTX
def initialize_api():
    return Api(
        app=None,
        version="1.0",
        title="PolyCapGlot API",
        description="API usada para manejar el acceso a videos y usuarios",
        doc="/docs/api-docs",
        default_swagger_filename="/docs/swagger"
    )

# Carga la configuración de Firebase desde un archivo JSON y la inicializa
def initialize_firebase():
    config = load_firebase_json()
    firebase_app = pyrebase.initialize_app(config)
    storage = firebase_app.storage()
    return firebase_app, storage

# Inicializar la base de datos
db = initialize_db()

# Inicializar la API
api = initialize_api()

# Inicializar Firebase
firebase, storage = initialize_firebase()

# Inicializar el procesador de videos
print("Start Process")
processor = None
processor = video_processor()
print("End Process")
