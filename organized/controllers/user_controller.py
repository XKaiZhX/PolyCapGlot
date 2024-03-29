from flask import request, jsonify
from flask_restx import Namespace, Resource

from extensions import db
from models.user_models import user_model, user_update_model, userDTO_public_model

user_controller = Namespace("user")

@user_controller.route("/")
class UserList(Resource):
    @user_controller.response(200, "Showing all users")
    @user_controller.marshal_with(userDTO_public_model)
    def get(self):
        '''
        Devuelve todos los DTO de los usuarios registrados
        '''
        return db.find_users()
    
    @user_controller.response(200, "User has been uploaded")
    @user_controller.response(400, "Username or email already exist")
    @user_controller.expect(user_model)
    @user_controller.marshal_with(userDTO_public_model)
    def post(self):
        '''
        Registra el usuario
        '''
        data = request.json
        if db.register_user(data):
            return data
        user_controller.abort(400, "Username or email already exist")
        
@user_controller.route("/<string:email>")
class User(Resource):
    @user_controller.response(200, "User has been deleted")
    @user_controller.response(404, "User not found")
    @user_controller.marshal_with(userDTO_public_model)
    def delete(self, email):
        found = db.delete_user_email(email)
        if found is not None:
            return found
        user_controller.abort(404, "User not found")

    @user_controller.response(200, "User has been uploaded")
    @user_controller.response(400, "Username already exist")
    @user_controller.response(404, "User not found")
    @user_controller.expect(user_update_model)
    def put(self, email):
        '''
        Registra el usuario
        '''
        data = request.json
        error = db.update_user(data, email)
        if error["value"] == 0:
            return (200, {"message": "updated correctly"})
        else:
            user_controller.abort(error["value"], error["message"])

    @user_controller.marshal_with(userDTO_public_model)
    def get(self, email):
        found = db.find_user_email(email)
        if found is not None:
            return found
        user_controller.abort(404, "User not found")