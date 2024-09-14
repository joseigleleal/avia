from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, save_response, verify_user, User, Session  # Asegúrate de importar User y Session
from werkzeug.security import generate_password_hash
from model import predict_fragility
import openai

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Permitir todos los orígenes

# Inicializar la base de datos
init_db()

# Configurar la clave de API de OpenAI
openai.api_key = 'YOUR_OPENAI_API_KEY'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if verify_user(username, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    user = User(username=username, password=hashed_password)

    session = Session()
    try:
        session.add(user)
        session.commit()
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 400
    finally:
        session.close()

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = predict_fragility(data)
    return jsonify({"prediction": prediction}), 200

@app.route('/api/save', methods=['POST'])
def save():
    data = request.json
    save_response(data)
    return jsonify({"message": "Response saved successfully"}), 201

@app.route('/api/predict_openai', methods=['POST'])
def predict_openai():
    data = request.json
    prompt = f"Predict fragility for the following data: {data}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    prediction = response.choices[0].text.strip()
    return jsonify({"prediction": prediction}), 200

if __name__ == '__main__':
    app.run(debug=True)