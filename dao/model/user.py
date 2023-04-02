from marshmallow import Schema, fields
from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    favorite_genre = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    surname = fields.Str()
    password = fields.Str()
    role = fields.Str()
    favorite_genre = fields.Str()

