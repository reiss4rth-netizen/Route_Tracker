import os
from flask_jwt_extended import current_user
import jwt
import requests
from functools import wraps
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from models import db, User, Trip, Stop

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trips.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['WEATHER_API_KEY'] = os.getenv("WEATHER_API_KEY")
app.config['ROUTES_API_KEY'] = os.getenv("ROUTES_API_KEY")
db.init_app(app)

HEADERS = {'User-Agent': 'UnforTrip/1.0'}

def get_coordinates_from_address(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
    response = requests.get(url, headers=HEADERS).json()
    if response.status_code == 200:
        return response[0]['lat'], response[0]['lon']
    return None, None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
            
        if not token:
            return jsonify({"error": "Token ausente, acceso denegado"}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({"error": "Usuario no encontrado"}), 401
        except Exception as e:
            return jsonify({"error": "Token inválido o expirado"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated


# Crear usuario
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    fields = ['name', 'username', 'email', 'password']
    if not all(field in data for field in fields):
        return jsonify ({"error" : "Faltan datos obligatorios"}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify ({"error" : "Nombre de usuario ya existente"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify ({"error" : "Ya hay una cuenta registrada con ese correo electrónico"}), 400
    
    try:
        new_user = User(
            name=data['name'],
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        token = jwt.encode({
            'user_id': new_user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)      
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"message": "Usuario registrado exitosamente", 
                    "user": new_user.to_json(),
                    "token": token
                    }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al registrar el usuario", "details": str(e)}), 500 
    
# Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)      
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"message": "Inicio de sesión exitoso", 
                    "user": user.to_json(),
                    "token": token
                    }), 200
    else:
        return jsonify({"error": "Nombre de usuario o contraseña incorrectos"}), 401   
    
# Editar usuario
@app.route('/api/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    if current_user.id != user_id:
        return jsonify({"error": "No autorizado para actualizar este usuario"}), 403
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    
    try:
        if 'name' in data:
            user.name = data['name']
        if 'username' in data:
            if User.query.filter_by(username=data['username']).first():
                return jsonify({"error": "Nombre de usuario ya existente"}), 400
            user.username = data['username']
        if 'email' in data:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({"error": "Ya hay una cuenta registrada con ese correo electrónico"}), 400
            user.email = data['email']
        
        db.session.commit()
        return jsonify({
            "message": "Usuario actualizado exitosamente", 
            "user": user.to_json()
            }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar el usuario", "details": str(e)}), 500
    
# Eliminar usuario
@app.route('/api/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    if current_user.id != user_id:
        return jsonify({"error": "No autorizado para eliminar este usuario"}), 403
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar el usuario", "details": str(e)}), 500
    
# Crear viaje 
@app.route('/api/trips', methods=['POST'])
@token_required
def create_trip(current_user):
    data = request.get_json(silent=True)
    if not data or not all(field in data for field in ['origin', 'destination', 'start_date', 'end_date']):
        return jsonify({"error": "Faltan datos obligatorios"}), 400