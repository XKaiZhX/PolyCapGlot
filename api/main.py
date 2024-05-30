from flask import Flask
from flask_cors import CORS
from extensions import api, secret_key
from controllers.user_controller import user_controller
from controllers.video_controller import video_controller
import logging


app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key

CORS(app)
#CORS(app, origins=["http://127.0.0.1:9002", "http://192.168.1.49:9002"])

api.init_app(app)

api.add_namespace(user_controller)
api.add_namespace(video_controller)
# End of file
if(__name__ == "__main__"):
    app.run("0.0.0.0", 9002, debug=True)