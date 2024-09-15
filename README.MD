# AVIA-AI: ALGORITMO DE VALIDACION DE INDEPENDENCIA Y AUTONOMIA

Este proyecto consiste en una aplicación que permite a los usuarios completar una encuesta sobre su salud y otros aspectos, y utiliza un modelo de machine learning para predecir la fragilidad. El proyecto se divide en dos partes principales: el backend y el frontend.

## Estructura del Proyecto

- `backend/` - Contiene la API que maneja la lógica del servidor, la conexión a la base de datos y el procesamiento de datos.
- `frontend/` - Contiene la interfaz de usuario construida con Streamlit que se comunica con el backend.

## Requisitos

### Backend

El backend utiliza Flask y SQLAlchemy para crear la API y manejar la base de datos. También utiliza `joblib` para cargar y guardar el modelo de machine learning.

#### Dependencias

Las dependencias para el backend están listadas en `backend/requirements.txt`.

### Frontend

El frontend está construido con Streamlit y utiliza `requests` para comunicarse con el backend.

#### Dependencias

Las dependencias para el frontend están listadas en `frontend/requirements.txt`.

## Configuración y Ejecución

### 1. Configurar el Backend

1. **Navega a la carpeta del backend:**
    ```bash
    cd backend
    ```

2. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Ejecuta el backend:**
    ```bash
    python app.py
    ```

   Esto iniciará el servidor Flask en `http://127.0.0.1:5000`.


4. **Crear Nuevos Usuarios**

      Puedes crear nuevos usuarios en el backend utilizando el siguiente comando:

    ```bash
    curl -X POST http://localhost:5000/api/add_user \
    -H "Content-Type: application/json" \
    -d '{"username": "user", "password": "pass"}'
   ```

### 2. Configurar el Frontend

1. **Navega a la carpeta del frontend:**
    ```bash
    cd frontend
    ```

2. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Ejecuta el frontend:**
    ```bash
    streamlit run app.py
    ```

   Esto abrirá la interfaz de usuario en tu navegador predeterminado.

## Descripción del Proyecto

### Backend

El backend proporciona una API RESTful que incluye las siguientes rutas:

- `/api/login` - Inicia sesión con credenciales de usuario.
- `/api/add_user` - Agrega un nuevo usuario a la base de datos.
- `/api/predict` - Realiza una predicción utilizando el modelo de machine learning.
- `/api/save` - Guarda las respuestas de la encuesta en la base de datos.
- `/api/predict_openai` - Realiza una predicción utilizando la API de OpenAI.

### Frontend

El frontend es una aplicación web construida con Streamlit que permite a los usuarios:

- Iniciar sesión.
- Completar una encuesta.
- Ver la predicción de fragilidad basada en sus respuestas.

## Contribución

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama nueva para tus cambios (`git checkout -b feature/your-feature`).
3. Realiza tus cambios y haz commit (`git commit -am 'Add new feature'`).
4. Empuja tus cambios a tu fork (`git push origin feature/your-feature`).
5. Crea un pull request para que tus cambios sean revisados.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Para cualquier pregunta o consulta, puedes contactarme en [desarrollojail@gmail.com](mailto:desarrollojail@gmail.com).
