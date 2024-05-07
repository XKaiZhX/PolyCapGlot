#El contenedor DEBE correr con este comando para comunicarse con el contenedor Mongo:
    #docker build -t docker_polycapglot .
    #docker run -p 9002:9002 -p 27017:27017 nombre_imagen

# Usa la imagen base de Python 3.9
FROM python:3.9

# Actualiza el sistema operativo e instala git
RUN apt-get update && \
    apt-get install -y git && \
    pip install --upgrade pip
    #pip install --upgrade setuptools\

# Clona el repositorio desde GitHub
RUN git clone https://github.com/XKaiZhX/PolyCapGlot.git /PolyCapGlot

# Establece el directorio de trabajo
WORKDIR /PolyCapGlot/api
RUN git checkout Andrew2

# Instala las dependencias de Python usando pip3 (por ejemplo, Flask)
RUN pip install -r requirements.txt

# Expone el puerto 9002 para acceder a la aplicación
EXPOSE 9002

# Define el comando de ejecución del contenedor
CMD ["python", "main.py"]