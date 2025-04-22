from app import db
from flask_login import UserMixin
from datetime import date

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # athlete, coach, admin

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)  # ⬅️ 新增這一行
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_announcement_coach_id'))