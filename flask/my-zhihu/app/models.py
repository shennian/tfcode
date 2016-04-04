from . import db


class User(db.Model):
    __tablenale__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer)
