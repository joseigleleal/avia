import pandas as pd
from database import Session, \
    Response  # Asegúrate de que 'database' es el nombre correcto del archivo donde tienes tu código de base de datos

# Cargar el archivo CSV en un DataFrame
csv_file_path = 'path/to/your/file.csv'
df = pd.read_csv(csv_file_path)

# Crear una sesión de base de datos
session = Session()

# Iterar sobre cada fila del DataFrame e insertar en la base de datos
for _, row in df.iterrows():
    # Convertir cada fila en un diccionario
    data = row.to_dict()

    # Crear una instancia de Response y agregarla a la sesión
    response = Response(**data)
    session.add(response)

# Confirmar los cambios y cerrar la sesión
session.commit()
session.close()
