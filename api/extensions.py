from mongoDB import MongoDB
from flask_restx import Api

db = MongoDB("mongodb://localhost:27017/")
api = Api(
    app=None,
    version="1.0",
    title="PolyCapGlot API",
    description="API usada para manejar el acces o a videos y usuarios",
    doc="/docs/api-docs",
    default_swagger_filename="/docs/swagger"
)

ai = None