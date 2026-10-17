import os
import jwt
import requests
from functools import wraps
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, User, Trip, Stop
from services import (
    token_required,
    get_coordinates_from_address,
    upload_file_to_s3,
    delete_file_from_s3,
    allowed_file
)

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trips.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['WEATHER_API_KEY'] = os.getenv("WEATHER_API_KEY")
app.config['ROUTES_API_KEY'] = os.getenv("ROUTES_API_KEY")
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

HEADERS = {'User-Agent': 'UnforTrip/1.0'}

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
@app.route('/api/user/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({"error": "No autorizado para actualizar este usuario"}), 403
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    
    try:
        if 'name' in data:
            name_val= str(data['name']).strip() if data['name'] is not None else ""
            if not name_val:
                return jsonify({
                    "error": "El nombre no puede estar vacío"
                }), 400
            user.name = name_val
        if 'username' in data:
            username_val = str(data['username']).strip() if data['username'] is not None else ""
            if not username_val:
                return jsonify({
                    "error": "El nombre de usuario no puede estar vacío"
                }),400
            existing_user = User.query.filter_by(username=username_val).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({
                    "error": "El nombre de usuario ya existe"
                }), 400
            user.username = username_val
        if 'email' in data:
            email_val = str(data['email']).strip() if data['email'] is not None else ""
            if not email_val:
                return jsonify({
                    "error": "El email no puede estar vacío"
                }), 400
            existing_email = User.query.filter_by(email=email_val).first()
            if existing_email and existing_email.id != user.id:
                return jsonify({
                    "error": "Este email ya esta en uso"
                }), 400
            user.email = email_val
        
        db.session.commit()
        return jsonify({
            "message": "Usuario actualizado exitosamente", 
            "user": user.to_json()
            }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar el usuario", 
                        "details": str(e)
                        }), 500
    
# Eliminar usuario
@app.route('/api/user/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
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
    if not data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    if not all(field in data for field in ['origin', 'destination', 'start_date']):
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    try:
        start_date_obj = datetime.strptime(data['start_date'], "%Y-%m-%d %H:%M:%S")
        distancia_simulation = 100.0  # Simulated distance in km
        duration_simulation = 120.0    # Simulated duration in minutes
        calculated_end_date = start_date_obj + timedelta(minutes=duration_simulation)
        
        new_trip = Trip(
            origin= data['origin'],
            destination= data['destination'],
            start_date= start_date_obj,
            end_date= calculated_end_date,
            distance_km= distancia_simulation,
            duration_minutes= duration_simulation,
            status= data.get('status', 'planned'),
            notes= data.get('notes'),
            user_id= current_user.id,
            is_public= data.get('is_public', False)
        )
        db.session.add(new_trip)
        db.session.flush()
        
        if 'stops' in data and isinstance(data['stops'], list):
            for index, stop_data in enumerate(data['stops']):
                new_stop = Stop(
                    name=stop_data.get('name'),
                    stop_type=stop_data.get('stop_type'), # Campo requerido añadido
                    latitude=stop_data.get('latitude'),
                    longitude=stop_data.get('longitude'),
                    stop_order=index,
                    description=stop_data.get('description'),
                    visited=stop_data.get('visited', False),
                    expected_weather=stop_data.get('expected_weather'),
                    last_weather_update=datetime.strptime(stop_data['last_weather_update'], "%Y-%m-%d %H:%M:%S") if 'last_weather_update' in stop_data else None,
                    trip_id=new_trip.id
            )
            db.session.add(new_stop)
        db.session.commit()
        return jsonify({
            "message": "Viaje creado exitosamente", 
            "trip": new_trip.to_json()
            }), 201
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use 'YYYY-MM-DD HH:MM:SS'"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear el viaje", "details": str(e)}), 500
    
# Eliminar un viaje
@app.route('/api/trips/<int:trip_id>', methods = ['DELETE'])
@token_required
def delete_trip(current_user, trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        return jsonify({
            "error": "No autorizado para eliminar este viaje"
        }), 403
    try:
        db.session.delete(trip)
        db.session.commit()
        return jsonify({
            "menssage": "Vieje eliminado con exito"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error al eliminar viaje", 
            "details": str(e)
        }), 500
        
# Cambiar foto de perfil
@app.route('/api/user/<int:user_id>/profile-photo', methods=['POST'])
@token_required
def upload_profile_picture(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({
            "error": "Acctión no autorizada"
            }), 403
    if 'profile_picture' not in request.files:
        return jsonify({
            "error": "No se envió ninguna imagen"
            }), 400
    file = request.files['profile_picture']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({
            "error": "Formato inválido"
            }), 400
    
    try:
        user = User.query.get_or_404(user_id)
        if user.profile_photo:
            delete_file_from_s3(user.profile_photo)
        
        file_url = upload_file_to_s3(file, folder='profiles')
        user.profile_photo = file_url
        db.session.commit()
        return jsonify({
            "message": "Foto de perfil actualizada",
            "profile_photo": file_url,
            "user": user.to_json()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error al subir la imagen",
            "details": str(e)
        })
        
@app.route('/api/user/<int:user_id>/profile-photo', methods=['DELETE'])
@token_required
def delete_profile_photo(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({
            "error": "Acción no autorizada"
        }), 403
    user = User.query.get_or_404(user_id)
    if not user.profile_photo:
        return jsonify({
            "error": "No hay una foto de perfil que borrar"
        }), 400
        
    try:
        delete_file_from_s3(user.profile_photo)
        user.profile_photo = None
        db.session.commit()
        return jsonify({
            "message": "Foto de perfil eliminada",
            "user": user.to_json()
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Error al eliminar",
            "details": str(e)
        }), 500
        
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)