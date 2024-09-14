import joblib
import numpy as np

# Cargar el modelo previamente entrenado
model = joblib.load('model.pkl')


def predict_fragility(data):
    # Preprocesar los datos según sea necesario
    features = np.array([[data['edad'], data['ingresos'], data['fatiga'], data['escalones'], data['caminar'],
                          len(data['enfermedades'].split(';')),
                          data['peso_perdido'], data['cronicas'], data['cardiovascular'], data['diabetes'],
                          data['epoc'], data['artrosis'],
                          data['osteoporosis'], data['incontinencia'], data['desordenes_mentales'], data['fuma'],
                          data['alcohol'], data['obesidad_abdominal'],
                          data['audicion'], data['vision'], data['miedo_caer'], data['estado_salud'], data['dolor'],
                          data['equilibrio'], data['test_silla'],
                          data['memoria'], data['sueno'], data['soledad'], data['redes_sociales'],
                          data['soporte_social']]])

    # Convertir las variables categóricas a variables dummy
    # Aquí deberías asegurarte de que las columnas coincidan con las que usaste para entrenar el modelo

    # Realizar la predicción
    prediction = model.predict(features)
    return prediction[0]
