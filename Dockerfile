# Usa la imagen de Python como base
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos
COPY app/requirements.txt ./backend/requirements.txt

# Instalar dependencias
RUN pip install --no-cache-dir -r app/requirements.txt

# Copiar todo el código al contenedor
COPY app/ ./backend/

# Copiar los archivos estáticos y templates al contenedor
COPY app/frontend/static ./frontend/static
COPY app/frontend/templates ./frontend/templates

# Exponer el puerto
EXPOSE 5001

# Comando para iniciar la aplicación
CMD ["python", "backend/app.py"]
