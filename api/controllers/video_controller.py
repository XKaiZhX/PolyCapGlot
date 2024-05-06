from flask import request, jsonify
from flask_restx import Namespace, Resource

from extensions import db, video_processor, storage, config
from services.user_service import UserService
from utils.service_utils import generate_video_hash, generate_translation_hash, generate_password_salt
from models.video_models import video_model, videoDTO_model, prerequest_model, request_model


user_service = UserService()
video_controller = Namespace("video")

@video_controller.route("/")
class VideoList(Resource):
    @video_controller.response(200, "Videos found")
    @video_controller.marshal_with(videoDTO_model)
    def get(self):
        '''
        Devuelve todos los DTO de los videos subidos
        '''
        return [] #! Usar MongoDB
    


@video_controller.route("/<string:id>")
class Video(Resource):
    @video_controller.response(200, "Video found")
    @video_controller.response(404, "Video not found")
    def get(self, id):
        '''
        Devuelve un video dado un id en la ruta
        '''
        found = None #TODO: USING MONGO
        if found is not None:
            return found
        video_controller.abort(404, f"Video with id {id} not found")

@video_controller.route("/request")
class VideoRequest(Resource):
    @video_controller.expect(prerequest_model)
    def post(self):
        '''
        Pre-request donde se devuelve si se puede subir el video o no
        '''
        data = request.json

        if user_service.find_one(data["email"]) is None:
            video_controller.abort(400, "email uploading not registered")

        generated = generate_video_hash(data["email"], data["title"], data["language"])
        uri = f"raw_videos/{generated}.mp4"

        proceed = db.preupload_video(data["email"], generated, data["title"], data["language"], uri) #TODO: Can it proceed or not process USING MONGO

        if proceed:
            
            return (
                    {
                        "message": "proceed", 
                        "firebase" : {
                            "uri": uri,
                            #? really needed? TODO: Autentification
                        }
                    }
                    )
        video_controller.abort(403, "Not able to proceed")

@video_controller.route("/upload")
class VideoUpload(Resource):
    @video_controller.expect(request_model)
    def post(self):
        data = request.json        
        
        email = data["email"]

        id = data["video_id"]
        filename = id #Hash de video

        sub = data["sub"] #Idioma del subtitulo

        #TODO: AUTENTIFICATION CHECK AND STUFF
        #! USER CHECKING NEEDED

        trans_id = generate_translation_hash(id, sub)

        #Database insertion
        if db.insert_translation(id, sub, trans_id) is False:
            video_controller.abort(400, "Error saving translation")

        video_found = db.find_video(id)

        #TODO: Descargar video desde firebase
        print("Descargando video de URI: ", video_found["firebase_uri"])

        storage.child(video_found["firebase_uri"]).download("", f"./temp/{id}.mp4")
        
        #print(storage.child(f"raw_videos/{id}.mp4").get_url(config["apiKey"]))

        #video_processor.process_video(filename, original, sub) #Lee desde /tmp/{id}.mp4, saca en /tmp/final_{id}.mp4

        #TODO: Descargar video desde firebase
        print("Subiendo video a URI: ", video_found["firebase_uri"])

        #video_processor.delete_files(filename)


