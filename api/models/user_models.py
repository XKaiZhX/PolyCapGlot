from flask_restx import fields
from extensions import api

user_dto_public_model = api.model(
    name="UserDTOPublic",
    model={
        "username": fields.String(required=True, description="Nombre del usuario"),
        "email": fields.String(required=True, description="Email del usuario")
    }
)

user_model = api.model(
    name="User",
    model={
        "username": fields.String(required=True, description="Nombre del usuario"),
        "email": fields.String(required=True, description="Email del usuario"),
        "password": fields.String(required=True, description="Contraseña del usuario")
    }
)

user_update_username_model = api.model(
    name="UserUpdateUsername",
    model={
        "email": fields.String(required=True, description="Email del usuario"),
        "username": fields.String(required=True, description="Nombre del usuario")
    }
)

user_password_model = api.model(
    name="UserUpdatePassword",
    model={
        "email": fields.String(required=True, description="Email del usuario"),
        "password": fields.String(required=True, description="Contraseña del usuario")
    }
)


'''
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

user_password_model = api.model(
    name="UserUpdatePassword",
    model={
        "email": fields.String(required=True, description="email del usuario"),
        "password": fields.String(required=True, description="password del usuario")
    }
)
'''