from mongoDB import MongoRepository
from flask_restx import Api

import pyrebase
import json

db = MongoRepository("mongodb://localhost:27017/")
api = Api(
    app=None,
    version="1.0",
    title="PolyCapGlot API",
    description="API usada para manejar el acces o a videos y usuarios",
    doc="/docs/api-docs",
    default_swagger_filename="/docs/swagger"
)

#Load firebase config from JSON
json_file = open("./config/firebase.json")
config = json.load(json_file)
json_file.close()

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

video_processor = None #MyVideoProcessor()