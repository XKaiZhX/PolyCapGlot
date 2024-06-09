from flask_restx import fields

from extensions import api

video_model = api.model(
    name="Video",
    model={
        "video_id": fields.String(required=True, description="Id del video"),
        "url": fields.String(required=True, description="URL del video"),
        "title": fields.String(required=True, description="Título del video"),
        "language": fields.String(required=True, description="Idioma del video")
    }
)

translation_model = api.model(
    name="Translation",
    model={
        "trans_id": fields.String(required=True, description="Id de la traduccion"),
        "video_id": fields.String(required=True, description="Id del video"),
        "url": fields.String(required=True, description="URL del video"),
        "language": fields.String(required=True, description="Idioma del video"),
        "status": fields.Integer(required=True, description="Estado de la traduccion, es 0 si está en proceso, 1 si ha terminado, -1 si ha fallado")
    }
)

videoDTO_model = api.model(
    name="VideoDTO",
    model={
        "url": fields.String(required=True, description="URL del video"),
        "title": fields.String(required=True, description="Título del video"),
        "language": fields.String(required=True, description="Idioma del video")
    }
)

prerequest_model = api.model(
    name="Prerequest",
    model={
        "title": fields.String(required=True, description="Titulo del video"),
        "language": fields.String(required=True, description="Idioma original del video")
    }
)

request_model = api.model(
    name="Request",
    model={
        "video_id": fields.String(required=True, description="Identificacion del video"),
        "sub": fields.String(required=True, description="Idioma de los subtitulos para video")
    }
)