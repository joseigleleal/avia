import joblib  # Biblioteca para serializar y deserializar modelos en Python
import numpy as np  # Biblioteca para trabajar con matrices y arreglos numéricos
from sklearn.ensemble import RandomForestClassifier  # Clasificador Random Forest de Scikit-learn
from sklearn.model_selection import train_test_split  # Función para dividir los datos en conjuntos de entrenamiento y prueba
from sklearn.datasets import make_classification  # Generador de conjuntos de datos de clasificación sintéticos

# Generar un conjunto de datos sintético para clasificación
# n_samples: número de muestras (1000)
# n_features: número de características (30)
# random_state: asegura la reproducibilidad
X, y = make_classification(n_samples=1000, n_features=30, random_state=42)

# Dividir los datos en conjuntos de entrenamiento (80%) y prueba (20%)
# random_state asegura que la división sea reproducible
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear una instancia del clasificador Random Forest
model = RandomForestClassifier()

# Entrenar el modelo usando los datos de entrenamiento
# X_train: características de entrenamiento
# y_train: etiquetas de entrenamiento
model.fit(X_train, y_train)

# Guardar el modelo entrenado en un archivo llamado 'model.pkl' usando joblib
joblib.dump(model, 'model.pkl')

# Imprimir un mensaje indicando que el modelo se ha entrenado y guardado correctamente
print("Modelo entrenado y guardado como 'model.pkl'")
