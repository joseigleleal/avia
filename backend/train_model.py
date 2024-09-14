import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification

# Generar datos de ejemplo
X, y = make_classification(n_samples=1000, n_features=30, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Guardar el modelo
joblib.dump(model, 'model.pkl')

print("Modelo entrenado y guardado como 'model.pkl'")
