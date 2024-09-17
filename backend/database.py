from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

# Crear un motor de base de datos usando SQLite y el archivo 'responses.db'
engine = create_engine('sqlite:///responses.db')

# Crear un generador de sesiones, atado al motor de la base de datos
Session = sessionmaker(bind=engine)


# Definir un modelo de usuario (tabla 'users')
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relación con el modelo Response
    responses = relationship("Response", back_populates="user")


# Definir un modelo de respuesta (tabla 'responses')
class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Relación con el modelo User
    user = relationship("User", back_populates="responses")

    # Definir todas las columnas según las preguntas del formulario de survey.html
    edad = Column(Integer, nullable=False)
    estado_civil = Column(String, nullable=False)
    sexo_nacimiento = Column(String, nullable=False)
    escolaridad = Column(String, nullable=False)  # Esta puede ser una lista separada por comas
    ocupacion = Column(String, nullable=False)
    ingresos = Column(String, nullable=False)

    # Escala FRAGIL
    fatiga = Column(Integer, nullable=False)
    escalones = Column(Integer, nullable=False)
    caminar = Column(Integer, nullable=False)
    enfermedades = Column(String)  # Puede ser una lista separada por comas

    # Pérdida de peso y fragilidad
    peso_perdido = Column(String, nullable=False)
    fragilidad = Column(String, nullable=False)

    # Hábitos y autopercepción de salud
    enfermedades_cronicas = Column(String, nullable=False)
    enfermedad_cardiovascular = Column(String, nullable=False)
    diabetes = Column(String, nullable=False)
    epoc = Column(String, nullable=False)
    artrosis = Column(String, nullable=False)
    osteoporosis = Column(String, nullable=False)
    incontinencia = Column(String, nullable=False)
    desordenes_mentales = Column(String, nullable=False)
    fuma = Column(String, nullable=False)
    alcohol = Column(String, nullable=False)
    obesidad_abdominal = Column(String, nullable=False)
    audicion = Column(String, nullable=False)
    vision = Column(String, nullable=False)
    miedo_caer = Column(String, nullable=False)
    estado_salud = Column(String, nullable=False)
    dolor = Column(String, nullable=False)
    problemas_equilibrio = Column(String, nullable=False)
    silla = Column(Integer, nullable=False)
    memoria = Column(String, nullable=False)
    sueño = Column(String, nullable=False)
    soledad = Column(String, nullable=False)
    uso_redes = Column(String, nullable=False)
    soporte_social = Column(String, nullable=False)

    # Estado Cognitivo (Mini-Cog)
    repeticion_palabras = Column(Integer, nullable=False)
    dibujo_reloj = Column(Integer, nullable=False)
    repeticion_puntuacion = Column(Integer, nullable=False)

    # Test de Cribado para Depresión
    depresion = Column(String)  # Lista separada por comas


# Inicializar la base de datos, creando todas las tablas definidas por los modelos
def init_db():
    Base.metadata.create_all(engine)


# Guardar una respuesta en la base de datos
def save_response(user_id, data):
    session = Session()
    response = Response(user_id=user_id, **data)
    session.add(response)
    session.commit()
    session.close()


# Registrar un nuevo usuario en la base de datos
def register_user(username, password):
    session = Session()
    hashed_password = generate_password_hash(password, method='sha256')
    user = User(username=username, password=hashed_password)
    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise Exception("El nombre de usuario ya está en uso.")
    finally:
        session.close()


# Verificar si un usuario existe y si la contraseña es correcta
def verify_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and check_password_hash(user.password, password):
        return True
    return False
