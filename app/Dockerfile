FROM python:3.9-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de requerimientos e instalarlos
COPY /requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia todo el contenido de la carpeta del proyecto dentro del contenedor
COPY . .

# Copiar la carpeta frontend (static y templates)
COPY frontend/templates /app/templates
COPY frontend/static /app/static

# Exponer el puerto que se utilizará
EXPOSE 5002

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:5002", "app:app"]