from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_photo = db.Column(db.String(512), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    trips = db.relationship('Trip', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "profile_photo": self.profile_photo,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    def to_public_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "profile_photo": self.profile_photo,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S")
        }
             
class Trip(db.Model):
    __tablename__ = 'trip'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    is_public = db.Column(db.Boolean, default=False)
    
    distance_km = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='planned')
    notes= db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    stops = db.relationship('Stop', backref='trip', lazy=True, cascade="all, delete-orphan",order_by="Stop.stop_order")
    media = db.relationship('Media', backref='trip', lazy=True, cascade="all, delete-orphan", foreign_keys='Media.trip_id')
    
    def to_json(self):
        return {
            "id": self.id,
            "origin": self.origin,
            "destination": self.destination,
            "start_date": self.start_date.strftime("%Y-%m-%d %H:%M:%S") if self.start_date else None,
            "end_date": self.end_date.strftime("%Y-%m-%d %H:%M:%S") if self.end_date else None,
            "is_public": self.is_public,
            "distance_km": self.distance_km,
            "duration_minutes": self.duration_minutes,
            "status": self.status,
            "notes": self.notes,
            "user_id": self.user_id,
            "stops": [stop.to_json() for stop in self.stops],
            "media": [m.to_json() for m in self.media] 
        }
        
class Stop(db.Model):
    __tablename__ = 'stop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    stop_type = db.Column(db.String(120), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    stop_order = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    visited = db.Column(db.Boolean, default=False)
    expected_weather = db.Column(db.String(120), nullable=True)
    last_weather_update = db.Column(db.DateTime, nullable=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    media = db.relationship('Media', backref='stop', lazy=True, cascade="all, delete-orphan", foreign_keys='Media.stop_id')
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "stop_type": self.stop_type,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "stop_order": self.stop_order,
            "description": self.description,
            "visited": self.visited,
            "expected_weather": self.expected_weather,
            "last_weather_update": self.last_weather_update.strftime("%Y-%m-%d %H:%M:%S") if self.last_weather_update else None,
            "trip_id": self.trip_id,
            "media": [m.to_json() for m in self.media]
        }

class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), nullable=False)
    media_type = db.Column(db.String(50), nullable=True, default='image')
    caption = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stop.id'), nullable=True)
    
    def to_json(self):
        return {
            "id": self.id,
            "url": self.url,
            "media_type": self.media_type,
            "caption": self.caption,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S") if self.date_created else None,
            "trip_id": self.trip_id,
            "stop_id": self.stop_id
        }