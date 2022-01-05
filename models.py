from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class client_entry(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(1000))
    state = db.Column(db.String(1000))
    last_checkin = db.Column(db.Integer)
