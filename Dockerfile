#El contenedor DEBE correr con estos comandos para comunicarse con el contenedor Mongo:

    #1
    #docker network create polycapglot_net

    #2
    #docker run --name pcg_mongo --network polycapglot_net -p 27017:27017 mongo

    #3
    #docker run --name api --network polycapglot_net -p 9002:9002 -v path/to/local/firebase.json:/PolyCapGlot/api/config/firebase.json -v path/to/local/deepl.json:/PolyCapGlot/api/config/deepl.json -v path/to/local/firebase_service.json:/PolyCapGlot/api/config/firebase_service.json docker_polycapglot
    #Andrew: docker run --name api --network polycapglot_net -p 9002:9002 -v C:\Users\NitroPC\Desktop\PolyCapGlot\Prototype\API\github/api/config/firebase.json:/PolyCapGlot/api/config/firebase.json -v C:\Users\NitroPC\Desktop\PolyCapGlot\Prototype\API\github/api/config/deepl.json:/PolyCapGlot/api/config/deepl.json -v C:\Users\NitroPC\Desktop\PolyCapGlot\Prototype\API\github/api/config/firebase_service.json:/PolyCapGlot/api/config/firebase_service.json docker_polycapglot

#Para buildear una imagen desde un Dockerfile:
    #docker build -t docker_polycapglot /path/to/Dockerfile --no-cache

#Para iniciar un api ya existente:
    #docker start api

#Para ejecutar un comando:
    #docker exec api sh -c "ls"

#Para ejecutar un comando con interaccion de usuario:
    #docker exec -it api nvim

# Usa la imagen base de Python 3.9
FROM python:3.9

# Actualiza el sistema operativo e instala varios paquetes
RUN apt-get update && \
    apt-get install -y git &&\
    apt-get install -y ffmpeg &&\
    apt-get install -y neovim &&\
    apt-get install -y cabextract &&\
    apt-get install -y wget &&\
    apt-get install -y imagemagick &&\
    apt-get install -y libmagick++-dev &&\
    apt-get install -y build-essential &&\
    apt-get install -y npm
    
RUN apt-get install -y nodejs

#Descargar fuentes (para Arial)
RUN mkdir /delete-me-fonts
WORKDIR /delete-me-fonts
RUN wget https://www.freedesktop.org/software/fontconfig/webfonts/webfonts.tar.gz
RUN tar -xzvf webfonts.tar.gz
RUN cabextract msfonts/*.exe
RUN cp *.ttf *.TTF /usr/share/fonts/
WORKDIR /
RUN rm -fr /delete-me-files

# Clona el repositorio desde GitHub
RUN git clone https://github.com/XKaiZhX/PolyCapGlot.git /PolyCapGlot

# Establece el directorio de trabajo
#! Quitar en un futuro para que se quede en Main
WORKDIR /PolyCapGlot/api
RUN git checkout Andrew3

# Instala las dependencias de Python del GitHub
RUN pip install -r requirements.txt
RUN pip install ffmpeg
#Cambios en configuracion de ImageMagick para que MoviePy funcione
RUN sed -i 's#<!-- <policy domain="cache" name="shared-secret" value="passphrase" stealth="true"/>#<!-- <policy domain="cache" name="shared-secret" value="passphrase" stealth="true"/> -->#' /etc/ImageMagick-6/policy.xml
RUN sed -i 's#<!-- in order to avoid to get image with password text -->#<!-- in order to avoid to get image with password text --><!--#' /etc/ImageMagick-6/policy.xml
RUN sed -i 's#<!-- disable ghostscript format types -->#--><!-- disable ghostscript format types -->#' /etc/ImageMagick-6/policy.xml

# Expone el puerto 9002 para acceder a la aplicación
EXPOSE 9002

#Define variable de entorno para que programa sepa si esta en contenedor
ENV IS_THIS_CONTAINER Yes

# Define el comando de ejecución del contenedor
CMD ["python", "main.py"]