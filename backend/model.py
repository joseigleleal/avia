import joblib  # Biblioteca para cargar modelos previamente guardados
import numpy as np  # Biblioteca para trabajar con arreglos numéricos

# Cargar el modelo previamente entrenado desde un archivo .pkl (Pickle)
# Este archivo debería haber sido creado durante el entrenamiento del modelo
model = joblib.load('model.pkl')


def predict_fragility(data):
    """
    Función para predecir la fragilidad de una persona basada en los datos de entrada.
    El modelo asume que los datos están en un formato específico y deben ser preprocesados antes de hacer la predicción.
    """

    # Convertir los datos de entrada en un arreglo de características (features)
    # Se extraen valores específicos de 'data' que se espera sean claves dentro de un diccionario.
    # Aquí se incluye la edad, ingresos, varios indicadores de salud y hábitos de la persona.
    features = np.array([[data['edad'], data['ingresos'], data['fatiga'], data['escalones'], data['caminar'],
                          len(data['enfermedades'].split(';')),
                          # Contar el número de enfermedades separadas por punto y coma
                          data['peso_perdido'], data['cronicas'], data['cardiovascular'], data['diabetes'],
                          data['epoc'], data['artrosis'],
                          # Variables booleanas (1 o 0) indicando presencia de estas condiciones
                          data['osteoporosis'], data['incontinencia'], data['desordenes_mentales'], data['fuma'],
                          data['alcohol'], data['obesidad_abdominal'],  # Indicadores de hábitos de vida o condiciones
                          data['audicion'], data['vision'], data['miedo_caer'], data['estado_salud'], data['dolor'],
                          data['equilibrio'], data['test_silla'],
                          # Variables relacionadas con la movilidad y estado físico
                          data['memoria'], data['sueno'], data['soledad'], data['redes_sociales'],
                          data['soporte_social']]])  # Factores sociales y de apoyo

    # Nota: Las variables categóricas, como 'estado_salud' o 'redes_sociales', que podrían ser strings,
    # deben ser convertidas en variables dummy (por ejemplo, usando one-hot encoding).
    # Aquí se asume que este paso ya fue realizado o no es necesario, pero en un entorno real, esto debe hacerse.
    # Asegúrate de que las características de entrada coincidan con las que usaste al entrenar el modelo.

    # Realizar la predicción con el modelo cargado
    prediction = model.predict(
        features)  # El modelo devuelve una predicción basada en las características proporcionadas

    return prediction[0]  # Devolver solo el primer valor de la predicción
