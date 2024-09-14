from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()
engine = create_engine('sqlite:///responses.db')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    feature1 = Column(String)
    feature2 = Column(String)
    # Agrega aquí todas las demás características que necesites

def init_db():
    Base.metadata.create_all(engine)

def save_response(data):
    session = Session()
    response = Response(**data)
    session.add(response)
    session.commit()
    session.close()


def register_user(username, password):
    session = Session()
    hashed_password = generate_password_hash(password, method='sha256')
    user = User(username=username, password=hashed_password)

    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        session.rollback()  # Deshacer la transacción en caso de error
        raise Exception("El nombre de usuario ya está en uso.")
    finally:
        session.close()

def verify_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and check_password_hash(user.password, password):
        return True
    return False
