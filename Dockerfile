#El contenedor DEBE correr con estos comandos para comunicarse con el contenedor Mongo:
    #docker build -t docker_polycapglot /path/to/Dockerfile --no-cache
    #docker network create polycapglot_net
    #docker run --name pcg_mongo --network polycapglot_net -p 27017:27017 mongo

    #docker run --name api --network polycapglot_net -p 9002:9002 -v path/to/local/firebase.json:/PolyCapGlot/api/config/firebase.json docker_polycapglot
    #docker run --name api --network polycapglot_net -p 9002:9002 -v C:\Users\NitroPC\Desktop\PolyCapGlot\Prototype\API\github/api/config/firebase.json:/PolyCapGlot/api/config/firebase.json -v C:\Users\NitroPC\Desktop\PolyCapGlot\Prototype\API\github/api/config/deepl.json:/PolyCapGlot/api/config/deepl.json docker_polycapglot

    #Para iniciar un api ya existente:
        #docker exec api find / -name "startup.sh"

# Usa la imagen base de Python 3.9
FROM python:3.9

# Actualiza el sistema operativo e instala git
RUN apt-get update && \
    apt-get install -y git &&\
    apt-get install -y ffmpeg
    
RUN apt-get install -y imagemagick
RUN apt-get install -y libmagick++-dev
RUN apt-get install -y build-essential

RUN pip install --upgrade pip &&\
    pip install --upgrade setuptools &&\
    pip install -U openai-whisper


# Clona el repositorio desde GitHub
RUN git clone https://github.com/XKaiZhX/PolyCapGlot.git /PolyCapGlot

# Establece el directorio de trabajo
WORKDIR /PolyCapGlot/api
RUN git checkout Andrew2

# Instala las dependencias de Python usando pip3 (por ejemplo, Flask)
RUN pip install -r requirements.txt

# Expone el puerto 9002 para acceder a la aplicación
EXPOSE 9002

#Define variable de entorno para que programa sepa si esta en contenedor
ENV IS_THIS_CONTAINER Yes

# Define el comando de ejecución del contenedor
CMD ["python", "main.py"]