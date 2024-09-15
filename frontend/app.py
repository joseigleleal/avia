import streamlit as st
import requests
import json

# URL del backend
API_URL = "http://127.0.0.1:5000"  # URL donde se encuentra el backend para interactuar con las APIs

# Función para iniciar sesión
def login(username, password):
    try:
        # Enviar una solicitud POST al endpoint de inicio de sesión con el nombre de usuario y la contraseña
        response = requests.post(f"{API_URL}/api/login", json={"username": username, "password": password})
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un código de estado HTTP 4xx/5xx
        return response.json()  # Retorna la respuesta en formato JSON
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")  # Muestra un error HTTP en la interfaz de usuario
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred: {err}")  # Muestra un error general en la interfaz de usuario
    except json.JSONDecodeError:
        st.error("Error decoding JSON response from server")  # Muestra un error si la respuesta no es JSON válido
    return None  # Retorna None en caso de error

# Función para guardar la respuesta
def save_response(data):
    try:
        # Enviar una solicitud POST al endpoint de guardado de datos con los datos de la encuesta
        response = requests.post(f"{API_URL}/api/save", json=data)
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un código de estado HTTP 4xx/5xx
        return response.json()  # Retorna la respuesta en formato JSON
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred while saving response: {http_err}")  # Muestra un error HTTP en la interfaz de usuario
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred while saving response: {err}")  # Muestra un error general en la interfaz de usuario
    except json.JSONDecodeError:
        st.error("Error decoding JSON response from server")  # Muestra un error si la respuesta no es JSON válido
    return None  # Retorna None en caso de error

# Función para realizar la predicción
def predict(data):
    try:
        # Enviar una solicitud POST al endpoint de predicción con los datos de la encuesta
        response = requests.post(f"{API_URL}/api/predict", json=data)
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un código de estado HTTP 4xx/5xx
        return response.json()  # Retorna la respuesta en formato JSON
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred while predicting: {http_err}")  # Muestra un error HTTP en la interfaz de usuario
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred while predicting: {err}")  # Muestra un error general en la interfaz de usuario
    except json.JSONDecodeError:
        st.error("Error decoding JSON response from server")  # Muestra un error si la respuesta no es JSON válido
    return None  # Retorna None en caso de error

# Manejo de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False  # Inicializa el estado de sesión si no está definido

# Página de inicio de sesión
if not st.session_state.logged_in:
    st.title("Iniciar Sesión")  # Título de la página de inicio de sesión
    username = st.text_input("Usuario")  # Campo para ingresar el nombre de usuario
    password = st.text_input("Contraseña", type="password")  # Campo para ingresar la contraseña (tipo 'password' oculta)

    if st.button("Iniciar Sesión"):
        response = login(username, password)  # Llama a la función de login
        if response and response.get("message") == "Login successful":
            st.session_state.logged_in = True  # Actualiza el estado de sesión a 'True' si el login es exitoso
            st.session_state.username = username  # Guarda el nombre de usuario en el estado de sesión
            st.success("Inicio de sesión exitoso")  # Muestra un mensaje de éxito
        else:
            st.error("Usuario o contraseña incorrectos")  # Muestra un mensaje de error si las credenciales son incorrectas
else:
    # Aquí comienza la lógica de la encuesta
    st.title("Reconquista escucha a sus adultos mayores")  # Título de la página de encuesta
    st.write("Esta encuesta nos permitirá conocer un poco más la situación de los adultos mayores en la ciudad de Reconquista, Santa Fe; de manera que podamos construir herramientas para predecir algunos aspectos críticos y evitarlos o retrasar su aparición.")  # Descripción de la encuesta

    # Sección 2: Datos Sociodemográficos
    st.header("Sección 2 de 6: Datos Sociodemográficos")  # Encabezado de la sección 2
    edad = st.number_input("1 - ¿Cuántos años tiene? (Edad en años)", min_value=0)  # Campo para ingresar la edad
    estado_civil = st.multiselect("2 - ¿Cuál es su estado civil?", ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Otro"], default=[])  # Campo para seleccionar el estado civil
    genero = st.multiselect("3 - Género autopercibido", ["Masculino", "Femenino", "Otro"], default=[])  # Campo para seleccionar el género autopercibido
    escolaridad = st.multiselect("4 - ¿Cuál es el grado de escolaridad máxima alcanzada?", ["Primaria incompleta", "Primaria completa", "Secundaria incompleta", "Secundaria completa", "Universitaria incompleta", "Universitaria completa"], default=[])  # Campo para seleccionar el grado de escolaridad
    ocupacion = st.text_input("5 - ¿Cómo definiría su ocupación a lo largo de su vida?")  # Campo para ingresar la ocupación
    ingresos = st.number_input("6 - ¿Cuáles son los ingresos mensuales de su hogar? (En pesos)")  # Campo para ingresar los ingresos mensuales

    # Sección 3: Escala FRAGIL
    st.header("Sección 3 de 6: Escala FRAGIL")  # Encabezado de la sección 3
    fatiga = st.multiselect("7 - ¿Qué parte del tiempo durante las últimas 4 semanas se sintió cansado/a?", ["Todo el tiempo", "La mayor parte del tiempo", "Parte del tiempo", "Nunca"], default=[])  # Campo para seleccionar la frecuencia de fatiga
    fatiga_score = 1 if any(item in fatiga for item in ["Todo el tiempo", "La mayor parte del tiempo"]) else 0  # Calcula el puntaje de fatiga

    escalones = st.multiselect("8 - ¿Tiene alguna dificultad para subir 10 escalones sin descansar?", ["Sí", "No"], default=[])  # Campo para seleccionar la dificultad para subir escalones
    escalones_score = 1 if "Sí" in escalones else 0  # Calcula el puntaje para dificultad al subir escalones

    caminar = st.multiselect("9 - ¿Tiene alguna dificultad para caminar 2 cuadras?", ["Sí", "No"], default=[])  # Campo para seleccionar la dificultad para caminar
    caminar_score = 1 if "Sí" in caminar else 0  # Calcula el puntaje para dificultad al caminar

    enfermedades = st.multiselect("10 - ¿Alguna vez un/a médico/a le dijo que tiene alguna de las siguientes enfermedades?", ["Hipertensión", "Diabetes", "Cáncer", "Enfermedad Pulmonar Crónica", "Ataque cardíaco", "Insuficiencia Cardíaca Congestiva", "Angina de Pecho", "Asma", "Artritis", "Ictus", "Enfermedad renal"], default=[])  # Campo para seleccionar enfermedades
    enfermedades_score = 1 if len(enfermedades) >= 5 else 0  # Calcula el puntaje para enfermedades

    peso_perdido = st.multiselect("11 - ¿Ha tenido pérdida de peso de forma involuntaria en el último año?", ["Sí", "No"], default=[])  # Campo para seleccionar pérdida de peso
    peso_perdido_score = 1 if "Sí" in peso_perdido else 0  # Calcula el puntaje para pérdida de peso

    total_score = fatiga_score + escalones_score + caminar_score + enfermedades_score + peso_perdido_score  # Calcula el puntaje total de la sección

    # Sección 4: Hábitos y Autopercepción de Salud
    st.header("Sección 4 de 6: Hábitos y Autopercepción de Salud")  # Encabezado de la sección 4
    cronicas = st.multiselect("12 - ¿Tiene antecedentes de enfermedades crónicas no transmisibles?", ["Sí", "No"], default=[])  # Campo para seleccionar antecedentes de enfermedades crónicas
    cardiovascular = st.multiselect("13 - ¿Tiene alguna enfermedad cardiovascular?", ["Sí", "No"], default=[])  # Campo para seleccionar enfermedades cardiovasculares
    diabetes = st.multiselect("14 - ¿Tiene diabetes?", ["Sí", "No"], default=[])  # Campo para seleccionar diabetes
    epoc = st.multiselect("15 - ¿Tiene EPOC?", ["Sí", "No"], default=[])  # Campo para seleccionar EPOC
    artrosis = st.multiselect("16 - ¿Tiene artrosis?", ["Sí", "No"], default=[])  # Campo para seleccionar artrosis
    osteoporosis = st.multiselect("17 - ¿Tiene osteoporosis?", ["Sí", "No"], default=[])  # Campo para seleccionar osteoporosis
    incontinencia = st.multiselect("18 - ¿Tiene incontinencia urinaria?", ["Sí", "No"], default=[])  # Campo para seleccionar incontinencia urinaria
    desordenes_mentales = st.multiselect("19 - ¿Padece desórdenes mentales?", ["Sí", "No"], default=[])  # Campo para seleccionar desórdenes mentales
    fuma = st.multiselect("20 - ¿Fuma?", ["Sí", "No"], default=[])  # Campo para seleccionar si fuma
    alcohol = st.multiselect("21 - ¿Consume alcohol?", ["Sí", "No"], default=[])  # Campo para seleccionar si consume alcohol
    obesidad_abdominal = st.multiselect("22 - ¿Tiene obesidad abdominal?", ["Sí", "No"], default=[])  # Campo para seleccionar obesidad abdominal
    audicion = st.multiselect("23 - Usted piensa que su audición es:", ["Buena", "Regular", "Mala"], default=[])  # Campo para seleccionar percepción de audición
    vision = st.multiselect("24 - Usted piensa que su visión es:", ["Buena", "Regular", "Mala"], default=[])  # Campo para seleccionar percepción de visión
    miedo_caer = st.multiselect("25 - ¿Usted tiene miedo a caerse?", ["Sí", "No"], default=[])  # Campo para seleccionar miedo a caídas
    estado_salud = st.selectbox("26 - ¿Cuál es su autopercepción de su estado de salud en general?", ["Muy bueno", "Bueno", "Regular", "Malo"])  # Campo para seleccionar autopercepción de salud
    dolor = st.multiselect("27 - Presencia de dolor", ["Sí", "No"], default=[])  # Campo para seleccionar presencia de dolor
    equilibrio = st.multiselect("28 - ¿Tiene o ha tenido problemas de equilibrio?", ["Sí", "No"], default=[])  # Campo para seleccionar problemas de equilibrio
    test_silla = st.number_input("29 - Test de la silla (segundos):", min_value=0, step=1)  # Campo para ingresar el resultado del test de la silla
    memoria = st.multiselect("30 - Autopercepción de la memoria", ["Buena", "Regular", "Mala"], default=[])  # Campo para seleccionar autopercepción de la memoria
    sueno = st.multiselect("31 - ¿Cómo piensa que es su sueño por las noches?", ["Bueno", "Regular", "Malo"], default=[])  # Campo para seleccionar percepción del sueño
    soledad = st.multiselect("32 - ¿Se siente solo?", ["Sí", "No"], default=[])  # Campo para seleccionar si se siente solo
    redes_sociales = st.selectbox("33 - ¿Cómo describiría su uso de redes sociales?", ["Frecuente", "Ocasional", "Inexistente"])  # Campo para seleccionar uso de redes sociales
    soporte_social = st.multiselect("34 - Usted diría que su soporte social es:", ["Bueno", "Regular", "Malo"], default=[])  # Campo para seleccionar soporte social

    # Sección 5: Estado cognitivo (mini cog)
    st.header("Sección 5 de 6: Estado cognitivo (mini cog)")  # Encabezado de la sección 5
    palabras_iniciales = st.text_input("35 - Enuncie tres palabras no relacionadas:")  # Campo para ingresar tres palabras no relacionadas
    test_reloj = st.text_area("36 - Dibuje la esfera de un reloj y coloque las manecillas en la hora indicada (11:10):")  # Campo para ingresar dibujo de reloj
    palabras_repetidas = st.text_input("37 - Repita las palabras que se le dieron al inicio:")  # Campo para ingresar las palabras repetidas

    # Sección 6: Test de Cribado para depresión
    st.header("Sección 6 de 6: Test de Cribado para depresión")  # Encabezado de la sección 6
    depresion = st.multiselect("38 - De los siguientes enunciados, ¿cuáles describen mejor su situación en las últimas 2 semanas?", ["Tengo poco apetito", "No puedo quitarme la tristeza", "Tengo dificultades para concentrarme", "Me sentí deprimido", "Duermo y no descanso", "Nada me hace feliz", "He perdido el interés en mis actividades", "Duermo mucho más de lo habitual", "Siento deseos de estar muerto", "Quiero hacerme daño", "Me siento cansado todo el tiempo"], default=[])  # Campo para seleccionar enunciados relacionados con la depresión

    # Pregunta final
    correo = st.text_input("Esta pregunta es opcional. Si desea recibir un informe con sus resultados, ingrese un correo electrónico:")  # Campo para ingresar un correo electrónico opcional

    # Botón de envío
    if st.button("Enviar encuesta"):
        # Crear un diccionario con los datos de la encuesta
        survey_data = {
            'edad': edad,
            'estado_civil': estado_civil,
            'genero': genero,
            'escolaridad': escolaridad,
            'ocupacion': ocupacion,
            'ingresos': ingresos,
            'fatiga': fatiga_score,
            'escalones': escalones_score,
            'caminar': caminar_score,
            'enfermedades': ';'.join(enfermedades),
            'peso_perdido': peso_perdido_score,
            'cronicas': cronicas,
            'cardiovascular': cardiovascular,
            'diabetes': diabetes,
            'epoc': epoc,
            'artrosis': artrosis,
            'osteoporosis': osteoporosis,
            'incontinencia': incontinencia,
            'desordenes_mentales': desordenes_mentales,
            'fuma': fuma,
            'alcohol': alcohol,
            'obesidad_abdominal': obesidad_abdominal,
            'audicion': audicion,
            'vision': vision,
            'miedo_caer': miedo_caer,
            'estado_salud': estado_salud,
            'dolor': dolor,
            'equilibrio': equilibrio,
            'test_silla': test_silla,
            'memoria': memoria,
            'sueno': sueno,
            'soledad': soledad,
            'redes_sociales': redes_sociales,
            'soporte_social': soporte_social,
            'palabras_iniciales': palabras_iniciales,
            'test_reloj': test_reloj,
            'palabras_repetidas': palabras_repetidas,
            'depresion': depresion,
            'correo': correo
        }

        # Guardar respuesta
        save_response(survey_data)  # Llama a la función para guardar los datos de la encuesta

        # Realizar predicción
        prediction = predict(survey_data)  # Llama a la función para obtener la predicción basada en los datos de la encuesta
        if prediction is not None:
            st.write(f"Predicción de fragilidad: {prediction['prediction']}")  # Muestra la predicción de fragilidad en la interfaz de usuario
        else:
            st.error("No se pudo obtener la predicción.")  # Muestra un mensaje de error si no se pudo obtener la predicción

        st.success("¡Gracias por completar la encuesta!")  # Muestra un mensaje de éxito tras enviar la encuesta

    # Botón de cierre de sesión
    if st.button("Cerrar Sesión"):
        st.session_state.logged_in = False  # Cambia el estado de sesión a 'False' para cerrar sesión
        st.success("Has cerrado sesión")  # Muestra un mensaje de éxito al cerrar sesión
