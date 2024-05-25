from flask import request, jsonify
from flask_restx import Namespace, Resource
import jwt
import datetime

from extensions import secret_key
from services.user_service import UserService
from utils.controller_utils import token_required, create_token
from models.user_models import user_model, user_update_username_model, user_password_model, userDTO_public_model

user_service = UserService()
user_controller = Namespace("user")

@user_controller.route("/")
class UserList(Resource):
    @user_controller.response(200, "Showing all users")
    @user_controller.marshal_with(userDTO_public_model)
    def get(self):
        '''
        Devuelve todos los DTO de los usuarios registrados
        '''
        return user_service.find_all()
    
    @user_controller.response(200, "User has been uploaded")
    @user_controller.response(400, "Email already exist")
    @user_controller.expect(user_model)
    @user_controller.marshal_with(userDTO_public_model)
    def post(self):
        '''
        Registra un usuario
        '''
        data = request.json
        if user_service.register(data["username"], data["email"], data["password"]):
            return data
        user_controller.abort(400, "Email already exist")

@user_controller.route("/<string:username>")
class UserUsernameList(Resource):
    @user_controller.response(200, "Showing users found")
    @user_controller.marshal_with(userDTO_public_model)
    def get(self, username):
        '''
        Devuelve todos los usuarios con el username
        '''
        return user_service.find_by_username(username)

@user_controller.route("/login")
class Login(Resource):
    @user_controller.expect(user_password_model)
    def post(self):
        '''
        Login
        '''
        data = request.json
        if(user_service.check_user_password(data["email"], data["password"])):

            found = user_service.find_one(email=data["email"])
            '''
            token = jwt.encode({
                'email': found['email'],
                'username': found['username'],
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=5)
                }, secret_key)
            '''
            token = create_token(found['email'], found['username'])
    
            return jsonify({'email': found["email"], 'username': found["username"], 'token': token})
        else:
            return user_controller.abort(403, "Wrong credentials")

@user_controller.route("/<string:email>")
class User(Resource):

    @user_controller.response(200, "User has been deleted")
    @user_controller.response(404, "User not found")
    @user_controller.marshal_with(userDTO_public_model)
    def delete(self, email):
        '''
        Borra a un usuario
        '''
        found = user_service.delete(email)
        if found is not None:
            return found
        user_controller.abort(404, "User not found")

    @user_controller.response(200, "User found")
    @user_controller.response(404, "User not found")
    @user_controller.marshal_with(userDTO_public_model)
    def get(self, email):
        '''
        Busca a un usuario
        '''
        found = user_service.find_one(email)
        if found is not None:
            return found
        user_controller.abort(404, "User not found")

@user_controller.route("/update/username")
class UserUpdateUsername(Resource):
    @user_controller.response(200, "User has been updated")
    @user_controller.response(404, "User not found")
    @user_controller.expect(user_update_username_model)
    def put(self):
        '''
        Actualiza el username del usuario
        '''
        data = request.json
        if user_service.update_username(data["email"], data["username"]):
            return ("User has been updated")
        else:
            user_controller.abort(404, "User not found")

@user_controller.route("/update/password")
class UserUpdatePassword(Resource):
    @user_controller.response(200, "User has been updated")
    @user_controller.response(404, "User not found")
    @user_controller.expect(user_password_model)
    def put(self):
        '''
        Actualiza el password del usuario
        '''
        data = request.json
        if user_service.update_password(data["email"], data["password"]):
            return ("User has been updated")
        else:
            user_controller.abort(404, "User not found")