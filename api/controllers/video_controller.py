from flask import request
from flask_restx import Namespace, Resource, reqparse
import logging

from extensions import storage, processor
from services.user_service import UserService
from services.video_service import VideoService
from utils.service_utils import (
    generate_video_hash, 
    generate_translation_hash, 
    generate_temp_folder, 
    check_file_exists
)
from utils.controller_utils import token_required, create_token, ns_log
from models.video_models import (
    video_dto_model, 
    prerequest_model, 
    request_model
)

# Instancias de los servicios de usuario y video
user_service = UserService()
video_service = VideoService()

# Creación del namespace para los controladores de video
video_controller = Namespace("video")

# Configuración de logging
fs = logging.FileHandler("./log/api.log")
video_controller.logger.addHandler(fs)
logging.basicConfig(level=logging.INFO)

@video_controller.route("/")
class VideoList(Resource):
    @video_controller.response(200, "Videos found")
    @video_controller.marshal_with(video_dto_model)
    def get(self):  #! SOLO PARA TESTEO
        '''
        Devuelve todos los DTO de los videos subidos
        '''
        ns_log(video_controller, "test", logging.CRITICAL)
        return []
    
    @token_required(video_controller)
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.param('video-id', 'Video to be deleted', 'header', required=True)
    def delete(self, current_user, **kwargs):
        '''
        Borra un video
        '''
        user = current_user
        headers = request.headers
        video_id = headers.get("video-id")

        # Logging para depuración
        print("deleting " + str(request.headers.get("video-id")))

        # Llamada al servicio de video para borrar el video
        result = video_service.delete_video(video_id, user["email"])
        if not result:
            ns_log(video_controller, "Failed to delete video " + str(video_id), logging.INFO)
            return False

        return True

@video_controller.route("/user")
class UserVideos(Resource):
    @token_required(video_controller)
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.response(200, "Video found")
    @video_controller.response(404, "Video not found")
    def post(self, current_user, **kwargs):
        '''
        Devuelve los videos del usuario actual
        '''
        user = current_user
        
        # Si el usuario no tiene videos, devolver una lista vacía
        if "videos" not in user:
            return []
        
        # Obtener la lista de videos del usuario
        video_list = video_service.get_user_videos(user["videos"])

        ns_log(video_controller, "videos fetched from user: " + user["email"], logging.INFO)
        return video_list

@video_controller.route("/request")
class VideoRequest(Resource):
    @token_required(video_controller)
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.expect(prerequest_model)
    def post(self, current_user, **kwargs):
        '''
        Pre-solicitud donde se determina si se puede subir el video o no
        '''
        data = request.json

        # Generar un hash único para el video
        generated = generate_video_hash(current_user["email"], data["title"], data["language"])
        uri = f"raw_videos/{generated}.mp4"

        # Pre-proceso de subida del video
        proceed = video_service.preupload_video(current_user["email"], generated, data["title"], data["language"], uri)

        if proceed:
            return {
                "token": create_token(current_user["email"], current_user["username"]),
                "uri": uri,
                "video_id": proceed["id"]
            }
        
        video_controller.abort(403, "Not able to upload video")

@video_controller.route("/upload")
class VideoUpload(Resource):
    @token_required(video_controller)
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.expect(request_model)
    def post(self, current_user, **kwargs):
        '''
        Sube un video a traducir
        '''
        data = request.json        

        video_id = data["video_id"]
        filename = video_id + ".mp4"  # Hash de video
        sub = data["sub"]  # Idioma del subtitulo
        
        trans_id = generate_translation_hash(video_id, sub)
        video_found = video_service.find_video(video_id)
        trans_found = video_service.find_translation(trans_id)

        if trans_found is not None:
            video_controller.abort(400, "Translation already exists")

        if video_found is None:
            video_controller.abort(404, "Video not found")

        try:
            folder_path = generate_temp_folder(video_id, video_found["language"], sub)
        except Exception as e:
            ns_log(video_controller, f"Translation already in process for video: {video_id} from " + current_user["email"], logging.INFO)
            video_controller.abort(404, "Translation already in process")

        ns_log(video_controller, "Descargando video de URI: " + video_found["firebase_uri"], logging.INFO)
        storage.child(video_found["firebase_uri"]).download("", f"{folder_path}/{video_id}.mp4")

        filepath = f"{folder_path}/{video_id}.mp4"

        if processor is not None:
            print("processing")
            filepath = processor.process_video(filename, folder_path, video_id, video_found["language"], sub)

        if not check_file_exists(filepath):
            msg = "non-existent file: " + filepath
            ns_log(video_controller, msg, logging.CRITICAL)
            video_service.delete_trans(trans_id, video_id)
            video_controller.abort(400, msg)

        ns_log(video_controller, "Subiendo video a URI: " + video_found["firebase_uri"], logging.INFO)
        storage.child(f"translated_videos/{trans_id}.mp4").put(filepath)

        # Inserción en la base de datos
        if not video_service.insert_translation(video_id, sub, trans_id):
            video_controller.abort(400, "Error saving translation")

        return {"message": "translation uploading"}

@video_controller.route("/translation")
class VideoTranslation(Resource):
    @token_required(video_controller)
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.param('video-id', 'video_id needed to confirm sender knows their relationship', 'header', required=True)
    @video_controller.param('trans-id', 'translation to be deleted', 'header', required=True)
    def delete(self, **kwargs):
        '''
        Borra una traducción de un video
        '''
        headers = request.headers

        trans_id = headers.get("trans-id")
        video_id = headers.get("video-id")

        print(str(video_id) + "$ - " + str(trans_id) + "$")
        result = video_service.delete_trans(trans_id, video_id)
        if not result:
            print("failed")
            return False

        return True


'''
from flask import request, jsonify
from flask_restx import Namespace, Resource, reqparse
import logging
import datetime

#from config.app_config import tmp_folder_path
from extensions import storage, processor
from services.user_service import UserService
from services.video_service import VideoService
from utils.service_utils import generate_video_hash, generate_translation_hash, generate_temp_folder, check_file_exists
from utils.controller_utils import token_required, create_token, ns_log
from models.video_models import video_model, translation_model, videoDTO_model, prerequest_model, request_model



user_service = UserService()
video_service = VideoService()
video_controller = Namespace("video")

fs = logging.FileHandler("./log/api.log")
video_controller.logger.addHandler(fs)
logging.basicConfig(level=logging.INFO)

@video_controller.route("/")
class VideoList(Resource):
    @video_controller.response(200, "Videos found")
    @video_controller.marshal_with(videoDTO_model)
    def get(self):  #! SOLO PARA TESTEO
        ''
        Devuelve todos los DTO de los videos subidos
        ''
        ns_log(video_controller, "test", logging.CRITICAL)
        return []
    
    @token_required(video_controller)
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.param('video-id', 'Video to be deleted', 'header', required=True)
    def delete(self, **kwargs):
        user = kwargs.get('current_user')
        headers = request.headers
        video_id = headers.get("video-id")

        print("deleting " + str(request.headers.get("video-id")))

        result = video_service.delete_video(video_id, user["email"])
        if result is False:
            ns_log(video_controller, "Failed to delete video " + str(video_id), logging.INFO)
            return False

        return True



@video_controller.route("/user")
class UserVideos(Resource):
    @token_required(video_controller)
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.response(200, "Video found")
    @video_controller.response(404, "Video not found")
    def post(self, **kwargs):
        user = kwargs.get('current_user')
            
        if "videos" not in user:
            return []
        
        video_list = video_service.get_user_videos(user["videos"])

        ns_log(video_controller, "videos fetched from user: " + user["email"], logging.INFO)
        return (video_list)
            
            


@video_controller.route("/request")
class VideoRequest(Resource):
    @token_required(video_controller)  # Ensure that the token is required for this endpoint
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.expect(prerequest_model)
    def post(self, current_user, **kwargs):
        ''
        Pre-request where it is determined if the video can be uploaded or not
        ''
        data = request.json

        generated = generate_video_hash(current_user["email"], data["title"], data["language"])
        uri = f"raw_videos/{generated}.mp4"

        proceed = video_service.preupload_video(current_user["email"], generated, data["title"], data["language"], uri)

        if proceed:
            return {
                "token": create_token(current_user["email"], current_user["username"]),
                "uri": uri,
                "video_id": proceed["id"]
            }
        
        video_controller.abort(403, "Not able to upload video")


@video_controller.route("/upload")
class VideoUpload(Resource):
    @token_required(video_controller)
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.expect(request_model)
    def post(self, current_user, **kwargs):
        data = request.json        

        id = data["video_id"]
        filename = id + ".mp4" #Hash de video
        sub = data["sub"] #Idioma del subtitulo
        
        trans_id = generate_translation_hash(id, sub)
        video_found = video_service.find_video(id)

        trans_found = video_service.find_translation(trans_id)

        if trans_found is not None:
            video_controller.abort(400, "Translation already exists")

        if video_found is None:
            video_controller.abort(404, "Video not found")

        try:
            folder_path = generate_temp_folder(id, video_found["language"], sub)
        except Exception as e:
            ns_log(video_controller, f"Translation already in process for video: {id} from " + current_user["email"], logging.INFO)
            video_controller.abort(404, "Translation already in process")

        ns_log(video_controller, "Descargando video de URI: " + video_found["firebase_uri"], logging.INFO)
        storage.child(video_found["firebase_uri"]).download("", f"{folder_path}/{id}.mp4")

        filepath = f"{folder_path}/{id}.mp4"

        if(processor is not None):
            print("processing")
            filepath = processor.process_video(filename, folder_path, id, video_found["language"], sub)

        if not check_file_exists(filepath):
            msg = "non-existent file: " + filepath
            ns_log(video_controller, msg, logging.CRITICAL)
            video_service.delete_trans(trans_id, id)
            video_controller.abort(400, msg)

        ns_log(video_controller, "Subiendo video a URI: " + video_found["firebase_uri"], logging.INFO)
        storage.child(f"translated_videos/{trans_id}.mp4").put(filepath)

        #video_processor.delete_files(filename)

        #Database insertion
        if video_service.insert_translation(id, sub, trans_id) is False:
            video_controller.abort(400, "Error saving translation")

        return {"message": "translation uploading"}

@video_controller.route("/translation")
class VideoTranslation(Resource):
    @token_required(video_controller)
    @video_controller.param('x-access-token', 'An access token', 'header', required=True)
    @video_controller.param('video_id', 'video_id needed to confirm sender knows their relationship', 'header', required=True)
    @video_controller.param('trans_id', 'translation to be deleted', 'header', required=True)
    def delete(self, **kwargs):

        headers = request.headers

        trans_id = headers.get("trans_id")
        video_id = headers.get("video_id")

        result = video_service.delete_trans(trans_id, video_id)
        if result is False:
            print("failed")
            return False

        return True
'''