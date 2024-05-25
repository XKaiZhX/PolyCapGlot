from flask import request, jsonify
from flask_restx import Namespace, Resource

from extensions import db, processor, storage, config
from services.user_service import UserService
from utils.service_utils import generate_video_hash, generate_translation_hash, generate_password_salt, generate_temp_folder, check_file_exists
from utils.controller_utils import token_required
from models.video_models import video_model, videoDTO_model, prerequest_model, request_model


user_service = UserService()
video_controller = Namespace("video")

original = ''

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

@video_controller.route("/user")
class UserVideos(Resource):
    @token_required
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.response(200, "Video found")
    @video_controller.response(404, "Video not found")
    def post(self, **kwargs):
        user = kwargs.get('current_user')
        expired = kwargs.get('is_expired')
        print(str(user) + "\nExpired: " + str(expired))

        try:
            video_list = []
            if "videos" not in user:
                raise Exception("user doesnt contain videos")
            for video_id in user["videos"]:
                video = db.find_video(video_id)
                video_list.append({
                    "title": video["title"],
                    "language": video["language"],
                    "firebase_uri": video["firebase_uri"],
                    "translations" : db.get_translations(video["id"])
                })

            print("videos: "+ str(video_list))
            return (video_list)
        except Exception as e:
            video_controller.abort(403, e)

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

        proceed = db.preupload_video(data["email"], generated, data["title"], data["language"], uri)

        if proceed:
            
            original = data["language"]

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
        filename = id + ".mp4" #Hash de video

        sub = data["sub"] #Idioma del subtitulo

        #TODO: AUTENTIFICATION CHECK AND STUFF
        #! USER CHECKING NEEDED

        trans_id = generate_translation_hash(id, sub)

        video_found = db.find_video(id)

        #TODO: Descargar video de firebase
        print("Descargando video de URI: ", video_found["firebase_uri"])

        generate_temp_folder()
        storage.child(video_found["firebase_uri"]).download("", f"./temp/{id}.mp4")

        processor.process_video(filename, id, video_found["language"], sub)
        check_file_exists(f"./temp/{id}_final.mp4")

        print("Subiendo video a URI: ", video_found["firebase_uri"])
        storage.child(f"translated_videos/{trans_id}.mp4").put(f"./temp/{id}_final.mp4") #TODO Generate translated video

        #video_processor.delete_files(filename)

        #Database insertion
        if db.insert_translation(id, sub, trans_id) is False:
            video_controller.abort(400, "Error saving translation")


