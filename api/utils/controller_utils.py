from functools import wraps
from flask import jsonify, request
from flask_restx import Namespace
from services.user_service import UserService
from extensions import api
from config.app_config import secret_key
from jwt import api_jws
import jwt
import datetime
import json
import logging

# Configuración y constantes
user_service = UserService()
TOKEN_DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"
LOG_DATEFORMAT = "[%d/%b/%Y %H:%M:%S] - "

# Funciones para el manejo de tokens
def create_token(email, username):
    """Crea un token JWT con expiración de 10 minutos."""
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=10)
    print(f"Expiration for token: {expiration}")
    token = jwt.encode(
        {"email": email, "username": username, "exp": str(expiration)},
        secret_key,
        algorithm="HS256"
    )
    return token

def decode_token(token):
    """Decodifica un token JWT y maneja errores comunes."""
    try:
        print("Payload: not decoded")
        payload = json.loads(api_jws.decode(token, secret_key, algorithms=["HS256"]).decode("utf-8"))
        print(f"Payload: {payload}")
        if datetime.datetime.now() > datetime.datetime.strptime(payload["exp"], TOKEN_DATEFORMAT):
            raise jwt.ExpiredSignatureError
        return payload
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        api.abort(403, "Token has expired")
    except jwt.InvalidTokenError:
        api.abort(403, "Token is invalid")
    except Exception as e:
        print(f"Token decoding error: {e}")
        raise Exception(f"Token decoding error: {e}")

# Decorador para verificar tokens
def token_required(ns: Namespace):
    """Decorador para rutas que requieren autenticación con token."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('x-access-token')
            if not token:
                msg = "Token is missing!"
                ns_log(ns, msg, logging.ERROR)
                api.abort(403, msg)
            try:
                print("Before decoding")
                decoded = decode_token(token)
                print("After decoding")
                user_id = decoded["email"]
                current_user = user_service.find_one(email=user_id)
                if not current_user:
                    msg = f"User not found: {user_id}"
                    ns_log(ns, msg, logging.ERROR)
                    api.abort(403, msg)
            except Exception as e:
                msg = f"Exception: {e}"
                ns_log(ns, msg, logging.ERROR)
                api.abort(403, msg)
            return f(*args, current_user=current_user, **kwargs)
        return decorated_function
    return decorator

# Función para registro de logs
def ns_log(ns: Namespace, msg: str, level: int):
    """Registra mensajes de log para un namespace dado."""
    ns.logger.log(level=level, msg=f"{datetime.datetime.now().strftime(LOG_DATEFORMAT)} {msg}")

# Función de traducción de video (placeholder)
def translate_video():
    """Función de traducción de video (a implementar)."""
    pass


'''
from functools import wraps
from flask import app, jsonify, request
from flask_restx import Namespace
from services.user_service import UserService
from extensions import api
from config.app_config import secret_key
from jwt import api_jws

import jwt
import datetime
import json
import logging

user_service = UserService()

token_dateformat = "%Y-%m-%d %H:%M:%S.%f"
log_dateformat = "[%d/%b/%Y %H:%M:%S] - "

def create_token(email, username):
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=10)
    print("expiration for token:" + str(expiration))
    token = jwt.encode({"email": email, "username": username, "exp": str(expiration)}, secret_key, algorithm="HS256")
    return token

def decode_token(token):
    try:
        print("payload: not decoded")
        payload = json.loads(api_jws.decode(token, secret_key, algorithms=["HS256"]).decode("utf-8"))
        print("payload: " + str(payload))
        if(datetime.datetime.now() > datetime.datetime.strptime(payload["exp"], token_dateformat)):
            raise jwt.ExpiredSignatureError
        return payload
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        api.abort(403, "Token has expired")
    except jwt.InvalidTokenError:
        api.abort(403, "Token is invalid")
    except Exception as e:
        # Handle other exceptions
        print(f"Token decoding error: {e}")
        raise Exception(f"Token decoding error: {e}")

def token_required(ns: Namespace):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('x-access-token')
            msg = "Token is missing!"
            if not token:
                ns_log(ns, msg, logging.ERROR)
                api.abort(403, msg)
            try:
                print("before decoding")
                decoded = decode_token(token)
                print("after decoding")
                user_id = decoded["email"]
                current_user = user_service.find_one(email=user_id)
                if not current_user:
                    msg = "User not found: " + user_id
                    ns_log(ns, msg, logging.ERROR)
                    api.abort(403, msg)
            except Exception as e:
                msg = "Exception: " + str(e)
                ns_log(ns, msg, logging.ERROR)
                api.abort(403, msg)
            # Pass current_user as a keyword argument
            return f(*args, current_user=current_user, **kwargs)
        return decorated_function
    return decorator

#Logging
def ns_log(ns: Namespace, msg: str, level: int):
    ns.logger.log(level=level, msg=datetime.datetime.now().strftime(log_dateformat) + msg)

#Translation
def translate_video():
    pass
'''