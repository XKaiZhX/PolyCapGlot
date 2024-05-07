from mongoDB import MongoRepository
from flask_restx import Api
from processor.core import video_processor

from utils.extension_utils import load_firebase_json, get_mongo_connection_string, configure_moviepy
import pyrebase
import json

db = MongoRepository(get_mongo_connection_string())
api = Api(
    app=None,
    version="1.0",
    title="PolyCapGlot API",
    description="API usada para manejar el acces o a videos y usuarios",
    doc="/docs/api-docs",
    default_swagger_filename="/docs/swagger"
)

#Load firebase config from JSON
config = load_firebase_json()

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

#deepl in this case


print("Start Process")
configure_moviepy()
processor = video_processor()
print("End Process")