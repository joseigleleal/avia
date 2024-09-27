from flask import Flask, request, jsonify, render_template, session, flash, redirect, url_for, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from database import init_db, save_response, verify_user, User, Session
import os
import requests
import json

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = 'Key_avia_ai'  # Cambia esto por una clave secreta real
CORS(app)

# Inicializar la base de datos al inicio
init_db()

# URL del app (puede que no se necesite si todo está en el mismo archivo)
API_URL = "http://localhost:5000"


# Ruta para servir el formulario HTML
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if verify_user(username, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Para solicitudes POST (pueden ser tanto desde un formulario como API)
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # Si el usuario ya está logueado, redirigir a la página de encuesta
    #if request.method == 'GET' and 'logged_in' in session and session['logged_in']:
    #    return redirect(url_for('survey_page'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = login(username, password)
        if isinstance(response, dict) and response.get("message") == "Login successful":
            session['logged_in'] = True
            session['username'] = username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('survey_page'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')

    return render_template('login.html')


@app.route('/survey')
def survey():
    return render_template('survey.html')


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
    form_data = request.json
    user_id = form_data.get('user_id')

    if not user_id:
        return jsonify({"error": "Falta el ID del usuario."}), 400

    save_user_response(user_id, form_data)

    return jsonify({"message": "Respuestas guardadas con éxito"}), 201


# Función para guardar respuestas
def save_user_response(user_id, form_data):
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
    fragilidad = "fragilidad moderada, Mejorar la actividad física y la dieta."
    recomendaciones = "Mejorar la actividad física y la dieta."
    return fragilidad, recomendaciones


@app.route('/procesar_edad', methods=['POST'])
def procesar_edad():
    edad = request.form.get('edad')
    edad = int(edad)

    reco = "No frágil"
    recomendacion = """
    Ante todo PACIENCIA, COMPRENSIÓN Y FLEXIBILIDAD

    El estado de fragilidad requiere un cuidado integral para no perder más autonomía e incluso intentar recuperarla. Para esto, es muy importante una tarea conjunta entre el adulto frágil y su red de cuidadores para garantizar la seguridad en el cuidado.
    1- Tener especial cuidado con la toma de medicación. ...
    7- Cuidar la piel. ...
    """

    rta = ""

    if edad > 60:
        rta = recomendacion
    else:
        rta = reco

    return f'{rta}'


# Ruta para servir archivos estáticos desde 'frontend/static'
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend/static', filename)


@app.route('/survey', methods=['GET', 'POST'])
def survey_page():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        survey_data = {
            'edad': request.form.get('edad'),
            'estado_civil': request.form.getlist('estado_civil'),
            'genero': request.form.getlist('genero'),
            'escolaridad': request.form.getlist('escolaridad'),
            'ocupacion': request.form.get('ocupacion'),
            'ingresos': request.form.get('ingresos'),
            'fatiga': int('todo_el_tiempo' in request.form.getlist('fatiga')) + int(
                'la_mayor_parte_del_tiempo' in request.form.getlist('fatiga')),
            'escalones': int('Sí' in request.form.getlist('escalones')),
            'caminar': int('Sí' in request.form.getlist('caminar')),
            'enfermedades': ';'.join(request.form.getlist('enfermedades')),
            'peso_perdido': int('Sí' in request.form.getlist('peso_perdido')),
            'cronicas': request.form.getlist('cronicas'),
            'cardiovascular': request.form.getlist('cardiovascular'),
            'diabetes': request.form.getlist('diabetes'),
            'epoc': request.form.getlist('epoc'),
            'artrosis': request.form.getlist('artrosis'),
            'osteoporosis': request.form.getlist('osteoporosis'),
            'incontinencia': request.form.getlist('incontinencia'),
            'desordenes_mentales': request.form.getlist('desordenes_mentales'),
            'fuma': request.form.getlist('fuma'),
            'alcohol': request.form.getlist('alcohol'),
            'obesidad_abdominal': request.form.getlist('obesidad_abdominal'),
            'audicion': request.form.getlist('audicion'),
            'vision': request.form.getlist('vision'),
            'miedo_caer': request.form.getlist('miedo_caer'),
            'estado_salud': request.form.getlist('estado_salud'),
            'dolor': request.form.getlist('dolor'),
            'problemas_equilibrio': request.form.getlist('problemas_equilibrio'),
            'silla': request.form.getlist('silla'),
            'memoria': request.form.getlist('memoria'),
            'sueño': request.form.getlist('sueño'),
            'soledad': request.form.getlist('soledad'),
            'uso_redes': request.form.getlist('uso_redes'),
            'soporte_social': request.form.getlist('soporte_social'),
            'repeticion_palabras': request.form.getlist('repeticion_palabras'),
            'dibujo_reloj': request.form.getlist('dibujo_reloj'),
            'repeticion_puntuacion': request.form.getlist('repeticion_puntuacion'),
            'depresion': request.form.getlist('depresion'),
        }
        submit_survey(survey_data)
        return redirect(url_for('thank_you_page'))

    return render_template('survey.html')


@app.route('/thank-you')
def thank_you_page():
    return render_template('thank_you.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Utiliza la variable de entorno PORT o 5001 por defecto
    app.run(host="0.0.0.0", port=port, debug=True)  # Permite que la app escuche en todas las interfaces
