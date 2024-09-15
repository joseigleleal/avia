from sqlalchemy import create_engine, Column, Integer, String  # SQLAlchemy para crear y definir modelos y columnas en la base de datos
from sqlalchemy.ext.declarative import declarative_base  # Base declarativa para definir clases de modelo
from sqlalchemy.exc import IntegrityError  # Excepción para manejar errores de integridad (como duplicados)
from sqlalchemy.orm import sessionmaker  # Creador de sesiones para interactuar con la base de datos
from werkzeug.security import generate_password_hash, check_password_hash  # Herramientas para generar y verificar contraseñas cifradas

# Crear una base declarativa para que las clases hereden de ella
Base = declarative_base()

# Crear un motor de base de datos usando SQLite y el archivo 'responses.db'
engine = create_engine('sqlite:///responses.db')

# Crear un generador de sesiones, atado al motor de la base de datos
Session = sessionmaker(bind=engine)

# Definir un modelo de usuario (tabla 'users')
class User(Base):
    __tablename__ = 'users'  # Nombre de la tabla
    id = Column(Integer, primary_key=True)  # Columna de ID, clave primaria
    username = Column(String, unique=True, nullable=False)  # Nombre de usuario, debe ser único y no nulo
    password = Column(String, nullable=False)  # Contraseña cifrada, no nula

# Definir un modelo de respuesta (tabla 'responses')
class Response(Base):
    __tablename__ = 'responses'  # Nombre de la tabla
    id = Column(Integer, primary_key=True)  # Columna de ID, clave primaria
    feature1 = Column(String)  # Columna para almacenar una característica (puedes agregar más)
    feature2 = Column(String)  # Otra columna de características
    # Agrega aquí todas las demás características que necesites

# Inicializar la base de datos, creando todas las tablas definidas por los modelos
def init_db():
    Base.metadata.create_all(engine)  # Crea las tablas en la base de datos si no existen

# Guardar una respuesta en la base de datos
def save_response(data):
    session = Session()  # Crear una nueva sesión para la transacción
    response = Response(**data)  # Crear una nueva instancia de respuesta con los datos proporcionados
    session.add(response)  # Agregar la respuesta a la sesión
    session.commit()  # Confirmar la transacción en la base de datos
    session.close()  # Cerrar la sesión

# Registrar un nuevo usuario en la base de datos
def register_user(username, password):
    session = Session()  # Crear una nueva sesión
    hashed_password = generate_password_hash(password, method='sha256')  # Cifrar la contraseña con SHA-256
    user = User(username=username, password=hashed_password)  # Crear una instancia de usuario con el nombre y la contraseña cifrada

    try:
        session.add(user)  # Intentar agregar el nuevo usuario a la base de datos
        session.commit()  # Confirmar la transacción si  va bien
    except IntegrityError:  # Manejar errores de integridad, como un nombre de usuario duplicado
        session.rollback()  # Deshacer la transacción en caso de error
        raise Exception("El nombre de usuario ya está en uso.")  # Lanzar una excepción si el nombre ya existe
    finally:
        session.close()  # Cerrar la sesión en cualquier caso (éxito o fallo)

# Verificar si un usuario existe y si la contraseña es correcta
def verify_user(username, password):
    session = Session()  # Crear una nueva sesión
    user = session.query(User).filter_by(username=username).first()  # Buscar el usuario en la base de datos por nombre
    session.close()  # Cerrar la sesión después de la consulta

    if user and check_password_hash(user.password, password):  # Si el usuario existe y la contraseña es correcta
        return True  # Autenticación exitosa
    return False  # Autenticación fallida si el usuario no existe o la contraseña es incorrecta
