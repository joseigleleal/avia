from flask import Flask, request, \
    jsonify  # Flask para crear la aplicación web, request para manejar solicitudes HTTP, y jsonify para retornar respuestas JSON
from flask_cors import CORS  # CORS para permitir solicitudes desde diferentes orígenes
from database import init_db, save_response, verify_user, User, \
    Session  # Funciones y clases relacionadas con la base de datos
from werkzeug.security import generate_password_hash  # Herramienta para generar contraseñas cifradas
from model import predict_fragility  # Función para hacer predicciones de fragilidad
import openai  # Biblioteca OpenAI para interactuar con sus modelos de IA

app = Flask(__name__)  # Crear la aplicación Flask
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Permitir todos los orígenes para rutas que comienzan con /api

# Inicializar la base de datos llamando a la función init_db que probablemente configura la base de datos
init_db()

# Configurar la clave de API de OpenAI para interactuar con su servicio
openai.api_key = 'YOUR_OPENAI_API_KEY'  # Clave de API necesaria para autenticarse con OpenAI


# Ruta para manejar el inicio de sesión de los usuarios
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json  # Obtener los datos en formato JSON de la solicitud
    username = data.get('username')  # Extraer el nombre de usuario del cuerpo de la solicitud
    password = data.get('password')  # Extraer la contraseña del cuerpo de la solicitud

    # Verificar si el usuario existe y la contraseña es correcta
    if verify_user(username, password):
        return jsonify({"message": "Login successful"}), 200  # Respuesta exitosa con código 200 (OK)
    else:
        return jsonify({"message": "Invalid credentials"}), 401  # Si falla, devolver un código 401 (No autorizado)


# Ruta para agregar un nuevo usuario
@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.json  # Obtener los datos de la solicitud en formato JSON
    username = data.get('username')  # Extraer el nombre de usuario
    password = data.get('password')  # Extraer la contraseña

    # Verificar que ambos campos estén presentes
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400  # Si faltan datos, retornar un error 400

    # Cifrar la contraseña utilizando SHA-256
    hashed_password = generate_password_hash(password, method='sha256')

    # Crear una nueva instancia de usuario
    user = User(username=username, password=hashed_password)

    # Crear una nueva sesión de base de datos
    session = Session()
    try:
        session.add(user)  # Agregar el nuevo usuario a la sesión
        session.commit()  # Confirmar la transacción en la base de datos
        return jsonify({"message": "User added successfully"}), 201  # Respuesta exitosa con código 201 (creado)
    except Exception as e:
        session.rollback()  # Si hay algún error, deshacer la transacción
        return jsonify({"message": str(e)}), 400  # Devolver el error con código 400 (Solicitud incorrecta)
    finally:
        session.close()  # Cerrar la sesión de la base de datos


# Ruta para hacer una predicción de fragilidad
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json  # Obtener los datos en formato JSON
    prediction = predict_fragility(data)  # Hacer la predicción llamando a la función correspondiente
    return jsonify({"prediction": prediction}), 200  # Devolver el resultado de la predicción con código 200 (OK)


# Ruta para guardar una respuesta en la base de datos
@app.route('/api/save', methods=['POST'])
def save():
    data = request.json  # Obtener los datos en formato JSON
    save_response(data)  # Llamar a la función para guardar los datos en la base de datos
    return jsonify({"message": "Response saved successfully"}), 201  # Responder con éxito indicando que se guardó


# Ruta para hacer una predicción usando el modelo de OpenAI
@app.route('/api/predict_openai', methods=['POST'])
def predict_openai():
    data = request.json  # Obtener los datos en formato JSON
    prompt = f"Predict fragility for the following data: {data}"  # Crear un prompt para enviar a OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",  # Utilizar el motor de OpenAI (en este caso text-davinci-003)
        prompt=prompt,  # Enviar el prompt con los datos
        max_tokens=50  # Limitar la respuesta a 50 tokens
    )
    prediction = response.choices[0].text.strip()  # Obtener la predicción del modelo y eliminar espacios en blanco
    return jsonify({"prediction": prediction}), 200  # Devolver la predicción con código 200 (OK)


# Ejecutar la aplicación en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)  # Iniciar el servidor Flask con el modo de depuración activado
