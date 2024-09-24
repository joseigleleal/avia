from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
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
    fragilidad=" fragilidad moderada, Mejorar la actividad física y la dieta."
    recomendaciones="Mejorar la actividad física y la dieta."
    return fragilidad, recomendaciones


@app.route('/procesar_edad', methods=['POST'])
def procesar_edad():
    edad = request.form.get('edad')
    edad = int(edad)

    reco= "No fragil"
    recomendacion = """
    Ante todo PACIENCIA, COMPRENSIÓN Y FLEXIBILIDAD

    El estado de fragilidad requiere un cuidado integral para no perder más autonomía e incluso intentar recuperarla. Para esto, es muy importante una tarea conjunta entre el adulto frágil y su red de cuidadores para garantizar la seguridad en el cuidado.
    1- Tener especial cuidado con la toma de medicación. El adulto frágil debe ser supervisado en la toma de la medicación prescripta. Sé flexible, si la persona mayor no quiere tomar su medicación puedes volver a intentarlo en otro momento. Dejá el horario a la vista; tratar de tener franjas horarias; asociar tomas con comidas; crear rutina. Evitá tomas nocturnas que alteren el sueño. No mezclen tratamientos sin la autorización del médico; evitar duplicar dosis.
    2- Colaborar en generar rutinas saludables. Evitar siestas prolongadas, no mirar televisión antes de dormir. Evitar comidas copiosas antes de acostarse. Estimule paseos al aire libre y la realización de actividades sociales y lúdicas
    3- Estimular la esfera cognitiva. Se pueden realizar juegos compartidos que estimulan el contacto social. Además, estimulan el lenguaje y generan sensación de satisfacción. Pueden ser juegos de mesa, sudoku, rompecabezas. Anotar fechas importantes, tachar aquellas que hayan pasado. Estimular conversaciones sin que parezcan evaluaciones
    4- Repartir tareas de cuidado. En caso de necesitarlo, contar con cuidador a tiempo parcial o permanente. El cuidador de una persona mayor dependiente debe procurar la participación activa de la persona cuidada, no sobreprotegiéndola ni haciendo cosas que él mismo pudiera hacer.
    5- Cuidar la higiene personal. La dificultad para el aseo es de las primeras alteraciones que presentan los adultos dependientes. Según el grado de dependencia se deberán establecer estrategias para el aseo. La ducha quedará reservada para quienes pueden bipedestación, la bañera si pueden ingresar y salir sin ayudas (se puede adaptar la bañera generando un ingreso sencillo). En caso de no poder utilizar esas estrategias, se realizará el aseo con asistencia en la cama.
    6- Prevenir caídas. Hay que tener especial cuidado con las caídas. Antes de comenzar a mover al adulto mayor, se deberá intentar que él lo pueda hacer por sus propios medios asistiéndolo verbalmente y ofreciendo apoyo que favorezca el movimiento. Por otro lado, si el adulto mayor puede caminar hay que evaluar la necesidad de asistencia con dispositivos. Es fundamental que esto último cuente con indicación clara de un especialista puesto que en muchos casos puede ser contraproducente.
    7- Cuidar la piel. En caso de incontinencia urinaria, corresponde realizar una consulta a un especialista ya que muchas veces se podría revertir. En caso de que la incontinencia fuera crónica y requiriese pañales se debe cambiar el pañal con regularidad (se recomienda al menos cada 4 hs), se debe limpiar y secar la piel antes de poner un pañal nuevo y utilizar cremas diseñadas para tal fin de forma tal que forme una barrera protectora en la piel y se reduzca la fricción y la humedad. En caso de estar postrado en cama, optimizar el cambio de pañales, utilizar dispositivos para evitar lesiones por presión (colchón antiescaras) y garantizar la rotación en la cama
    """

    rta = ""

    if edad > 60:
        rta = recomendacion
    else:
        rta = reco

    return f'{rta}'


@app.route('/generar_json', methods=['POST'])
def generar_json():
    # Obtener todos los datos del formulario
    data = {}
    for key, value in request.form.items():
        data[key] = value

    # Puedes aplicar alguna lógica adicional antes de devolver la respuesta

    # Devuelve los datos como JSON
    return jsonify(data)


# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('data/datarec.csv')

df = df.fillna("Valor por defecto")  # Rellena datos faltantes con un valor específico

# Verificar que el DataFrame se haya creado correctamente
#print(df)

@app.route('/generar_informe', methods=['POST'])
def generar_informe():
    # Obtener todos los datos del formulario
    respuestas = {}
    for key, value in request.form.items():
        respuestas[key] = value

    recomendaciones = []
    servicios = []

    # Mapeo de las preguntas a las etiquetas
    preguntas_a_etiquetas = {
        "¿Tiene diagnóstico de hipertensión arterial?": "13. recomendaciones de ejercicio",
        "¿Tiene angina de pecho?": "13. recomendaciones de ejercicio",
        "¿Tiene insuficiencia cardiaca?": "13. recomendaciones de ejercicio",
        "¿Ha tenido alguna vez un infarto?": "13. recomendaciones de ejercicio",
        "¿Ha tenido ACV?": "13. recomendaciones de ejercicio",
        "¿Tiene diagnóstico de diabetes?": "9. Diabetes",
        "¿Tiene EPOC?": "10. EPOC",
        "¿Tiene artrosis?": "11. Artrosis",
        "¿Tiene osteoporosis?": "14. Osteoporosis",
        "¿Tiene incontinencia urinaria?": "16. Incontinencia urinaria",
        "¿Padece desórdenes mentales?": "17. Salud mental",
        "¿Fuma?": "1. Fumar",
        "¿Consume alcohol?": "2. Alcohol",
        "¿Tiene obesidad abdominal?": "5. Obesidad",
        "¿Usted piensa que su audición es?": "8. Audición",
        "¿Usted piensa que su visión es?": "7. Visión",
        "¿Se ha caído alguna vez en el último año?": "15. Movilidad",
        "¿Cuál es su autopercepción de su estado de salud en general?": "12. dolor",
        "¿Cómo piensa que es su sueño por las noches?": "19. sueño",
        "¿Se siente solo?": "18. salud emocional",
        "¿Cómo describiría su uso de redes sociales?": "20. RRSS"
    }

    # Iterar sobre las respuestas y buscar recomendaciones y servicios
    for pregunta, respuesta in respuestas.items():
        if pregunta in preguntas_a_etiquetas:
            etiqueta = preguntas_a_etiquetas[pregunta]
            # Filtrar el DataFrame por la etiqueta
            row = df[df['Etiquetas'] == etiqueta]
            if not row.empty:
                recomendaciones.append(row['Recomendación'].values[0])
                servicios.append(row['Servicios'].values[0])

    # Generar el disclaimer
    disclaimer = ("Estas recomendaciones de salud fueron generadas con la ayuda de inteligencia artificial."
                  " Bajo ningún concepto son reemplazo de la evaluación por un profesional de la salud. "
                  "Le recomendamos realizar consultas de salud periódicas con clínica médica o gerontología "
                  "para poder elaborar un plan de cuidado.")

    # Crear el informe
    informe = {
        "Recomendaciones": "\n".join(recomendaciones),
        "Servicios": "\n".join(servicios),
        "Disclaimer": disclaimer
    }

    return jsonify(informe)


# Ruta para servir archivos estáticos desde 'frontend/static'
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend/static', filename)


if __name__ == '__main__':
    app.run(debug=True)
