from flask_restx import fields

from extensions import api

userDTO_public_model = api.model(
    name="UserDTOPublic",
    model={
        "username": fields.String(required=True, description="nombre del usuario"),
        "email": fields.String(required=True, description="email del usuario")
    }
)

user_model = api.model(
    name="User",
    model={
        "username": fields.String(required=True, description="nombre del usuario"),
        "email": fields.String(required=True, description="email del usuario"),
        "password": fields.String(required=True, description="password del usuario")
    }
)

user_update_username_model = api.model(
    name="UserUpdateUsername",
    model={
        "email": fields.String(required=True, description="email del usuario"),
        "username": fields.String(required=True, description="nombre del usuario")
    }
)

user_update_password_model = api.model(
    name="UserUpdatePassword",
    model={
        "email": fields.String(required=True, description="email del usuario"),
        "password": fields.String(required=True, description="password del usuario")
    }
)