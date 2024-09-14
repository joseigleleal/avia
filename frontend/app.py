import streamlit as st
import requests
import json

# URL del backend
API_URL = "http://127.0.0.1:5000"


# Función para iniciar sesión
def login(username, password):
    try:
        response = requests.post(f"{API_URL}/api/login", json={"username": username, "password": password})
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred: {err}")
    except json.JSONDecodeError:
        st.error("Error decoding JSON response from server")
    return None

# Función para guardar la respuesta
def save_response(data):
    try:
        response = requests.post(f"{API_URL}/api/save", json=data)
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred while saving response: {http_err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred while saving response: {err}")
    except json.JSONDecodeError:
        st.error("Error decoding JSON response from server")
    return None  # Asegúrate de devolver None en caso de error

# Función para realizar la predicción
def predict(data):
    try:
        response = requests.post(f"{API_URL}/api/predict", json=data)
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred while predicting: {http_err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred while predicting: {err}")
    except json.JSONDecodeError:
        st.error("Error decoding JSON response from server")
    return None  # Asegúrate de devolver None en caso de error

# Manejo de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Página de inicio de sesión
if not st.session_state.logged_in:
    st.title("Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        response = login(username, password)
        if response and response.get("message") == "Login successful":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Inicio de sesión exitoso")
        else:
            st.error("Usuario o contraseña incorrectos")
else:
    # Aquí comienza la lógica de la encuesta
    st.title("Reconquista escucha a sus adultos mayores")
    st.write(
        "Esta encuesta nos permitirá conocer un poco más la situación de los adultos mayores en la ciudad de Reconquista, Santa Fe; de manera que podamos construir herramientas para predecir algunos aspectos críticos y evitarlos o retrasar su aparición.")

    # Sección 2: Datos Sociodemográficos
    st.header("Sección 2 de 6: Datos Sociodemográficos")
    edad = st.number_input("1 - ¿Cuántos años tiene? (Edad en años)", min_value=0)
    estado_civil = st.multiselect("2 - ¿Cuál es su estado civil?",
                                  ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Otro"], default=[])
    genero = st.multiselect("3 - Género autopercibido", ["Masculino", "Femenino", "Otro"], default=[])
    escolaridad = st.multiselect("4 - ¿Cuál es el grado de escolaridad máxima alcanzada?",
                                 ["Primaria incompleta", "Primaria completa", "Secundaria incompleta",
                                  "Secundaria completa", "Universitaria incompleta", "Universitaria completa"],
                                 default=[])
    ocupacion = st.text_input("5 - ¿Cómo definiría su ocupación a lo largo de su vida?")
    ingresos = st.number_input("6 - ¿Cuáles son los ingresos mensuales de su hogar? (En pesos)")

    # Sección 3: Escala FRAGIL
    st.header("Sección 3 de 6: Escala FRAGIL")
    fatiga = st.multiselect("7 - ¿Qué parte del tiempo durante las últimas 4 semanas se sintió cansado/a?",
                            ["Todo el tiempo", "La mayor parte del tiempo", "Parte del tiempo", "Nunca"], default=[])
    fatiga_score = 1 if any(item in fatiga for item in ["Todo el tiempo", "La mayor parte del tiempo"]) else 0

    escalones = st.multiselect("8 - ¿Tiene alguna dificultad para subir 10 escalones sin descansar?",
                               ["Sí", "No"], default=[])
    escalones_score = 1 if "Sí" in escalones else 0

    caminar = st.multiselect("9 - ¿Tiene alguna dificultad para caminar 2 cuadras?",
                             ["Sí", "No"], default=[])
    caminar_score = 1 if "Sí" in caminar else 0

    enfermedades = st.multiselect(
        "10 - ¿Alguna vez un/a médico/a le dijo que tiene alguna de las siguientes enfermedades?",
        ["Hipertensión", "Diabetes", "Cáncer", "Enfermedad Pulmonar Crónica", "Ataque cardíaco",
         "Insuficiencia Cardíaca Congestiva", "Angina de Pecho", "Asma", "Artritis", "Ictus",
         "Enfermedad renal"], default=[])  # Sin opción seleccionada por defecto
    enfermedades_score = 1 if len(enfermedades) >= 5 else 0

    peso_perdido = st.multiselect("11 - ¿Ha tenido pérdida de peso de forma involuntaria en el último año?",
                                  ["Sí", "No"], default=[])
    peso_perdido_score = 1 if "Sí" in peso_perdido else 0

    total_score = fatiga_score + escalones_score + caminar_score + enfermedades_score + peso_perdido_score

    # Sección 4: Hábitos y Autopercepción de Salud
    st.header("Sección 4 de 6: Hábitos y Autopercepción de Salud")
    cronicas = st.multiselect("12 - ¿Tiene antecedentes de enfermedades crónicas no transmisibles?",
                              ["Sí", "No"], default=[])
    cardiovascular = st.multiselect("13 - ¿Tiene alguna enfermedad cardiovascular?",
                                    ["Sí", "No"], default=[])
    diabetes = st.multiselect("14 - ¿Tiene diabetes?",
                              ["Sí", "No"], default=[])
    epoc = st.multiselect("15 - ¿Tiene EPOC?",
                          ["Sí", "No"], default=[])
    artrosis = st.multiselect("16 - ¿Tiene artrosis?",
                              ["Sí", "No"], default=[])
    osteoporosis = st.multiselect("17 - ¿Tiene osteoporosis?",
                                  ["Sí", "No"], default=[])
    incontinencia = st.multiselect("18 - ¿Tiene incontinencia urinaria?",
                                   ["Sí", "No"], default=[])
    desordenes_mentales = st.multiselect("19 - ¿Padece desórdenes mentales?",
                                         ["Sí", "No"], default=[])
    fuma = st.multiselect("20 - ¿Fuma?",
                          ["Sí", "No"], default=[])
    alcohol = st.multiselect("21 - ¿Consume alcohol?",
                             ["Sí", "No"], default=[])
    obesidad_abdominal = st.multiselect("22 - ¿Tiene obesidad abdominal?",
                                        ["Sí", "No"], default=[])
    audicion = st.multiselect("23 - Usted piensa que su audición es:", ["Buena", "Regular", "Mala"], default=[])
    vision = st.multiselect("24 - Usted piensa que su visión es:", ["Buena", "Regular", "Mala"], default=[])
    miedo_caer = st.multiselect("25 - ¿Usted tiene miedo a caerse?",
                                ["Sí", "No"], default=[])
    estado_salud = st.selectbox("26 - ¿Cuál es su autopercepción de su estado de salud en general?",
                                ["Muy bueno", "Bueno", "Regular", "Malo"])
    dolor = st.multiselect("27 - Presencia de dolor",
                           ["Sí", "No"], default=[])
    equilibrio = st.multiselect("28 - ¿Tiene o ha tenido problemas de equilibrio?",
                                ["Sí", "No"], default=[])
    test_silla = st.number_input("29 - Test de la silla (segundos):", min_value=0, step=1)
    memoria = st.multiselect("30 - Autopercepción de la memoria", ["Buena", "Regular", "Mala"], default=[])
    sueno = st.multiselect("31 - ¿Cómo piensa que es su sueño por las noches?",
                           ["Bueno", "Regular", "Malo"], default=[])
    soledad = st.multiselect("32 - ¿Se siente solo?",
                             ["Sí", "No"], default=[])
    redes_sociales = st.selectbox("33 - ¿Cómo describiría su uso de redes sociales?",
                                  ["Frecuente", "Ocasional", "Inexistente"])
    soporte_social = st.multiselect("34 - Usted diría que su soporte social es:",
                                    ["Bueno", "Regular", "Malo"], default=[])

    # Sección 5: Estado cognitivo (mini cog)
    st.header("Sección 5 de 6: Estado cognitivo (mini cog)")
    palabras_iniciales = st.text_input("35 - Enuncie tres palabras no relacionadas:")
    test_reloj = st.text_area("36 - Dibuje la esfera de un reloj y coloque las manecillas en la hora indicada (11:10):")
    palabras_repetidas = st.text_input("37 - Repita las palabras que se le dieron al inicio:")

    # Sección 6: Test de Cribado para depresión
    st.header("Sección 6 de 6: Test de Cribado para depresión")
    depresion = st.multiselect(
        "38 - De los siguientes enunciados, ¿cuáles describen mejor su situación en las últimas 2 semanas?",
        ["Tengo poco apetito", "No puedo quitarme la tristeza", "Tengo dificultades para concentrarme",
         "Me sentí deprimido", "Duermo y no descanso", "Nada me hace feliz",
         "He perdido el interés en mis actividades", "Duermo mucho más de lo habitual",
         "Siento deseos de estar muerto", "Quiero hacerme daño", "Me siento cansado todo el tiempo"], default=[])

    # Pregunta final
    correo = st.text_input(
        "Esta pregunta es opcional. Si desea recibir un informe con sus resultados, ingrese un correo electrónico:")

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
        save_response(survey_data)

        # Realizar predicción
        prediction = predict(survey_data)
        if prediction is not None:
            st.write(f"Predicción de fragilidad: {prediction['prediction']}")
        else:
            st.error("No se pudo obtener la predicción.")

        st.success("¡Gracias por completar la encuesta!")

    if st.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.success("Has cerrado sesión")