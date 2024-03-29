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

user_update_model = api.model(
    name="UserUpdate",
    model={
        "username": fields.String(required=True, description="nombre del usuario"),
        "email": fields.String(required=True, description="email del usuario"),
        "password": fields.String(required=True, description="password del usuario"),
        "operation": fields.String(required=True, description="nombre del campo a actualizar"),
    }
)