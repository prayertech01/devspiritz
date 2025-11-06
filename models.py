from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Sermon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    preacher = db.Column(db.String(100))
    date_preached = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.Text)
    audio_file = db.Column(db.String(200))
    video_file = db.Column(db.String(200))
    notes = db.Column(db.Text)

class GalleryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    image = db.Column(db.String(200))
    video = db.Column(db.String(200))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
