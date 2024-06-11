from flask import Flask
from flask_cors import CORS
from extensions import api
from config.app_config import secret_key
from controllers.user_controller import user_controller
from controllers.video_controller import video_controller

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secret_key

    # Configuración de CORS
    CORS(app)
    
    # Inicialización de la API
    api.init_app(app)

    # Añadir namespaces (controladores) a la API
    api.add_namespace(user_controller)
    api.add_namespace(video_controller)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=9002, debug=True)
