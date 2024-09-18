from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'Key_avia_ai'  # Cambia esto por una clave secreta real

# URL del backend
API_URL = "http://127.0.0.1:5000"


# Función para iniciar sesión
def login(username, password):
    try:
        response = requests.post(f"{API_URL}/api/login", json={"username": username, "password": password})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as err:
        return f"Error occurred: {err}"
    except json.JSONDecodeError:
        return "Error decoding JSON response from server"


# Función para guardar la respuesta
def save_response(data):
    try:
        response = requests.post(f"{API_URL}/api/save", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred while saving response: {http_err}"
    except requests.exceptions.RequestException as err:
        return f"Error occurred while saving response: {err}"
    except json.JSONDecodeError:
        return "Error decoding JSON response from server"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/')
def index():
    return 'Página de inicio'

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Limpiar la sesión
    return redirect(url_for('index'))  # Redirigir a la página principal o de inicio

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('survey_page'))

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

# Función para realizar la predicción
def predict(data):
    try:
        response = requests.post(f"{API_URL}/api/predict", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred while predicting: {http_err}"
    except requests.exceptions.RequestException as err:
        return f"Error occurred while predicting: {err}"
    except json.JSONDecodeError:
        return "Error decoding JSON response from server"

@app.route('/survey', methods=['GET', 'POST'])
def survey_page():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        # Obtener datos del formulario
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
            'estado_salud': request.form.get('estado_salud'),
            'dolor': request.form.getlist('dolor'),
            'equilibrio': request.form.getlist('equilibrio'),
            'test_silla': request.form.get('test_silla'),
            'memoria': request.form.getlist('memoria'),
            'sueno': request.form.getlist('sueno'),
            'soledad': request.form.getlist('soledad'),
            'redes_sociales': request.form.get('redes_sociales'),
            'soporte_social': request.form.getlist('soporte_social'),
            'palabras_iniciales': request.form.get('palabras_iniciales'),
            'test_reloj': request.form.get('test_reloj'),
            'palabras_repetidas': request.form.get('palabras_repetidas'),
            'depresion': request.form.getlist('depresion'),
            'correo': request.form.get('correo')
        }

        # Guardar respuesta
        save_response(survey_data)

        # Realizar predicción
        prediction = predict(survey_data)
        if prediction is not None:
            flash(f"Predicción de fragilidad: {prediction.get('prediction')}", 'success')
        else:
            flash('No se pudo obtener la predicción.', 'error')

        return render_template('success.html')

    return render_template('survey.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001,debug=True)
