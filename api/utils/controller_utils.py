
from functools import wraps
from flask import app, jsonify, request
from flask_restx import Namespace
from services.user_service import UserService
from extensions import api, secret_key
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

def token_required(f):
    @wraps(f)
    def decorated_function(ns: Namespace, *args, **kwargs):
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
            expired = datetime.datetime.now() > datetime.datetime.strptime(decoded["exp"], token_dateformat)
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
        return f(*args, current_user=current_user, is_expired=expired, **kwargs)
    return decorated_function

#Logging

def ns_log(ns: Namespace, msg: str, level: int):
    ns.logger.log(level=level, msg=datetime.datetime.now().strftime(log_dateformat) + msg)