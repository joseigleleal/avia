from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from database import init_db, save_response, verify_user, User, Session

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Inicializar la base de datos al inicio
init_db()

# Ruta para servir el formulario HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

# Ruta para manejar el inicio de sesión de los usuarios
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if verify_user(username, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Ruta para agregar un nuevo usuario
@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    user = User(username=username, password=hashed_password)
    session = Session()

    try:
        session.add(user)
        session.commit()
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 400
    finally:
        session.close()

# Ruta para guardar una respuesta en la base de datos
@app.route('/api/save', methods=['POST'])
def save():
    data = request.json
    save_response(data)
    return jsonify({"message": "Response saved successfully"}), 201

# Ruta para procesar la encuesta
@app.route('/api/submit-survey', methods=['POST'])
def submit_survey():
    """
    Ruta para manejar el envío de la encuesta.
    Se espera que los datos de la encuesta lleguen en formato JSON.
    """
    try:
        form_data = request.json  # Cambiado a request.json
        user_id = form_data.get('user_id')

        if not user_id:
            return jsonify({"error": "Falta el ID del usuario."}), 400

        save_user_response(user_id, form_data)

        return jsonify({"message": "Respuestas guardadas con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Función para guardar respuestas
def save_user_response(user_id, form_data):
    """
    Función que guarda las respuestas de la encuesta en la base de datos.
    :param user_id: ID del usuario que envía la respuesta
    :param form_data: Diccionario con los datos del formulario
    """
    response_data = {
        'edad': form_data.get('edad'),
        'estado_civil': form_data.get('estado_civil'),
        'sexo_nacimiento': form_data.get('sexo_nacimiento'),
        'escolaridad': form_data.get('escolaridad'),
        'ocupacion': form_data.get('ocupacion'),
        'ingresos': form_data.get('ingresos'),
        'fatiga': form_data.get('fatiga'),
        'escalones': form_data.get('escalones'),
        'caminar': form_data.get('caminar'),
        'enfermedades': form_data.get('enfermedades'),
        'peso_perdido': form_data.get('peso_perdido'),
        'fragilidad': form_data.get('fragilidad'),
        'enfermedades_cronicas': form_data.get('enfermedades_cronicas'),
        'enfermedad_cardiovascular': form_data.get('enfermedad_cardiovascular'),
        'diabetes': form_data.get('diabetes'),
        'epoc': form_data.get('epoc'),
        'artrosis': form_data.get('artrosis'),
        'osteoporosis': form_data.get('osteoporosis'),
        'incontinencia': form_data.get('incontinencia'),
        'desordenes_mentales': form_data.get('desordenes_mentales'),
        'fuma': form_data.get('fuma'),
        'alcohol': form_data.get('alcohol'),
        'obesidad_abdominal': form_data.get('obesidad_abdominal'),
        'audicion': form_data.get('audicion'),
        'vision': form_data.get('vision'),
        'miedo_caer': form_data.get('miedo_caer'),
        'estado_salud': form_data.get('estado_salud'),
        'dolor': form_data.get('dolor'),
        'problemas_equilibrio': form_data.get('problemas_equilibrio'),
        'silla': form_data.get('silla'),
        'memoria': form_data.get('memoria'),
        'sueño': form_data.get('sueño'),
        'soledad': form_data.get('soledad'),
        'uso_redes': form_data.get('uso_redes'),
        'soporte_social': form_data.get('soporte_social'),
        'repeticion_palabras': form_data.get('repeticion_palabras'),
        'dibujo_reloj': form_data.get('dibujo_reloj'),
        'repeticion_puntuacion': form_data.get('repeticion_puntuacion'),
        'depresion': form_data.get('depresion'),
    }

    save_response(user_id, response_data)

# Ruta para hacer una predicción usando el modelo de OpenAI
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json

    # Mock de la predicción de fragilidad
    mock_prediction = {
        "fragilidad": "moderada",
        "recomendaciones": "Mejorar la actividad física y la dieta."
    }

    return jsonify({"prediction": mock_prediction}), 200

# Ruta para servir archivos estáticos desde 'frontend/static'
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend/static', filename)

if __name__ == '__main__':
    app.run(debug=True)
