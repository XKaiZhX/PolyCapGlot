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

# Actualiza el sistema operativo e instala varios paquetes
RUN apt-get update && \
    apt-get install -y git &&\
    apt-get install -y ffmpeg &&\
    apt-get install -y neovim &&\
    apt-get install -y cabextract &&\
    apt-get install -y wget &&\
    apt-get install -y imagemagick &&\
    apt-get install -y libmagick++-dev &&\
    apt-get install -y build-essential

#Descargar fuentes (para Arial)
RUN mkdir /delete-me-fonts
WORKDIR /delete-me-fonts
RUN wget https://www.freedesktop.org/software/fontconfig/webfonts/webfonts.tar.gz
RUN tar -xzvf webfonts.tar.gz
RUN cabextract msfonts/*.exe
RUN cp *.ttf *.TTF /usr/share/fonts/
WORKDIR /
RUN rm -fr /delete-me-files

#RUN echo "deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty multiverse deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates multiverse deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-backports main restricted universe multiverse" | tee /etc/apt/sources.list.d/multiverse.list
#RUN apt-get install -y software-properties-common
#RUN apt-get install -y aptitude
#RUN echo "deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty multiverse" >> /etc/apt/sources.list.d/multiverse.list && \
#    echo "deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates multiverse" >> /etc/apt/sources.list.d/multiverse.list && \
#    echo "deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-backports main restricted universe multiverse" >> /etc/apt/sources.list.d/multiverse.list
#    apt-get update --allow-insecure-repositories
#RUN apt-add-repository multiverse
#RUN apt-get update --allow-insecure-repositories
#RUN aptitude install -y ttf-mscorefonts-installer
        
#TODO: Añadir paquetes al requirements.txt
RUN pip install --upgrade pip &&\
    pip install --upgrade setuptools &&\
    pip install torchvision &&\
    pip install -U openai-whisper


# Clona el repositorio desde GitHub
RUN git clone https://github.com/XKaiZhX/PolyCapGlot.git /PolyCapGlot

# Establece el directorio de trabajo
WORKDIR /PolyCapGlot/api
RUN git checkout Andrew2 #! Quitar en un futuro para que se quede en Main

# Instala las dependencias de Python usando pip3 (por ejemplo, Flask)
RUN pip install -r requirements.txt

#Recuerda cambiar el XML el path raro ese de MoviePy
        #docker exec -it api nvim /etc/ImageMagick-6/policy.xml
#Cambios en ImageMagick para que no explote
RUN sed -i 's#<!-- <policy domain="cache" name="shared-secret" value="passphrase" stealth="true"/>#<!-- <policy domain="cache" name="shared-secret" value="passphrase" stealth="true"/> -->#' /etc/ImageMagick-6/policy.xml
RUN sed -i 's#<!-- in order to avoid to get image with password text -->#<!-- in order to avoid to get image with password text --><!--#' /etc/ImageMagick-6/policy.xml
RUN sed -i 's#<!-- disable ghostscript format types -->#--><!-- disable ghostscript format types -->#' /etc/ImageMagick-6/policy.xml
# Expone el puerto 9002 para acceder a la aplicación
EXPOSE 9002

#Define variable de entorno para que programa sepa si esta en contenedor
ENV IS_THIS_CONTAINER Yes

# Define el comando de ejecución del contenedor
CMD ["python", "main.py"]