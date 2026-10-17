import os
import jwt
import uuid
import boto3
import requests
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import User
from dotenv import load_dotenv
load_dotenv()

ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg', 'webp'}
BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")
SECRET_KEY = os.getenv("SECRET_KEY")

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=REGION
)

# ----Authentication----
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
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({"error": "Usuario no encontrado"}), 401
        except Exception as e:
            return jsonify({"error": "Token inválido o expirado"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# ---Geolocation---
HEADERS = {'User-Agent': 'UnforTrip/1.0'}

def get_coordinates_from_address(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

# ---Multimedia (AWS S3)---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def upload_file_to_s3(file, folder="profiles"):
    filename = secure_filename(file.filename)
    unique_filename = f"{folder}/{uuid.uuid4()}_{filename}"
    
    s3_client.upload_fileobj(
        file,
        BUCKET_NAME,
        unique_filename,
        ExtraArgs={"ContentType": file.content_type}
    )
    return f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{unique_filename}"

def delete_file_from_s3(file_url):
    if not file_url:
        return
    try:
        key = file_url.split(".amazonaws.com/")[-1]
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)
    except Exception:
        pass