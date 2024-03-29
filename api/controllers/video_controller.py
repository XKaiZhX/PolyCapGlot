from flask import request, jsonify
from flask_restx import Namespace, Resource

from extensions import db
from utils.controller_utils import generate_hash, generate_firebase
from models.video_models import video_model, videoDTO_model, prerequest_model

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

        if db.find_user_email(data["email"]) is None:
            #video_controller.abort(404, "email uploading not registered")
            pass
        generated = generate_hash(data["email"], data["title"], data["language"])

        proceed = db.preupload_video(generated) #TODO: Can it proceed or not process USING MONGO

        if proceed:
            
            return (
                    {
                        "message": "proceed", 
                        "firebase" : {
                            "uri": "INSERT_FIREBASE_URI",
                            "bucket": "INSERT_FIREBASE_BUCKET",
                            #TODO: Autentification
                        }
                    }
                    ) #? Maybe I can return the Firebase URL from here so the client doesn't store it? On Android perhaps, on React IDK
        video_controller.abort(403, "Not able to proceed")


class VideoUpload(Resource):
    pass