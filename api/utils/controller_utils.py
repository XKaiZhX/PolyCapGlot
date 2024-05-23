
from functools import wraps
from flask import app, jsonify, request
from services.user_service import UserService
from extensions import api, secret_key
from jwt import api_jws

import jwt
import datetime
import json

user_service = UserService()

dateformat = "%Y-%m-%d %H:%M:%S.%f"

def create_token(email, username):
    expiration = datetime.datetime.now() + datetime.timedelta(seconds=10)
    print("expiration for token:" + str(expiration))
    token = jwt.encode({"email": email, "username": username, "exp": str(expiration)}, secret_key, algorithm="HS256")
    return token

def decode_token(token):
    try:
        print("payload: not decoded")
        payload = json.loads(api_jws.decode(token, secret_key, algorithms=["HS256"]).decode("utf-8"))
        print("payload: " + str(payload))
        if(datetime.datetime.now() > datetime.datetime.strptime(payload["exp"], dateformat)):
            raise jwt.ExpiredSignatureError
        return payload
    except jwt.ExpiredSignatureError:
        api.abort(403, "Token has expired")
    except jwt.InvalidTokenError:
        api.abort(403, "Token is invalid")
    except Exception as e:
        # Handle other exceptions
        print(f"Token decoding error: {e}")
        raise Exception(f"Token decoding error: {e}")

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            print("Token missing")
            api.abort(403, "Token is missing!")
        try:
            print("before decoding")
            decoded = decode_token(token)
            print("after decoding")
            user_id = decoded["email"]
            expired = datetime.datetime.now() > datetime.datetime.strptime(decoded["exp"], dateformat)
            current_user = user_service.find_one(email=user_id)
            if not current_user:
                print("User not found")
                api.abort(403, "User not found")
        except Exception as e:
            print("Exception: " + str(e))
            api.abort(403, str(e))
        # Pass current_user as a keyword argument
        return f(*args, current_user=current_user, is_expired=expired, **kwargs)
    return decorated_function