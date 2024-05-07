#El contenedor DEBE correr con este comando para comunicarse con el contenedor Mongo: docker run -p 9002:9002 -p 27017:27017 nombre_imagen

# Usa la imagen base de Python 3.8
FROM python:3.8

# Actualiza el sistema operativo e instala git
RUN apt-get update && \
    apt-get install -y git

# Clona el repositorio desde GitHub
RUN git clone https://github.com/XKaiZhX/PolyCapGlot.git /PolyCapGlot
RUN git checkout ZhenKai

# Establece el directorio de trabajo
WORKDIR /PolyCapGlot/api

# Instala las dependencias de Python usando pip3 (por ejemplo, Flask)
RUN pip install -r requirements.txt

# Expone el puerto 9002 para acceder a la aplicación
EXPOSE 9002

# Define el comando de ejecución del contenedor
CMD ["python", "main.py"]