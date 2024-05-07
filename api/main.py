from flask import Flask

from extensions import api
from controllers.user_controller import user_controller
from controllers.video_controller import video_controller

app = Flask(__name__)

api.init_app(app)

api.add_namespace(user_controller)
api.add_namespace(video_controller)
# End of file
if(__name__ == "__main__"):
    app.run("0.0.0.0", 9002, debug=True)