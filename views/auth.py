import calendar
import datetime
import hashlib
import base64
import jwt
from flask import request, abort
from flask_restx import Resource, Namespace
from config import Config
from dao.model.user import User
from setup_db import db

auth_namespace = Namespace('auth')


@auth_namespace.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get('username')
        password = req_json.get('password')

        if password is None or username is None:
            abort(401)

        user = db.session.query(User).filter(User.username == username).first()

        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        hash_password = base64.b64encode(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),  Config.PWD_HASH_SALT, Config.PWD_HASH_ITERATIONS))
        if hash_password != user.password:
            return {"error": "Неверные учётные данные"}, 401

        data = {'username': username,
                'role': user.role}

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        tokens = {'access_token': access_token, 'refresh_token': refresh_token}

        return tokens

    def put(self):
        req_json = request.json
        refresh_token = req_json.get('refresh_token')

        if refresh_token is None:
            abort(401)

        try:
            data = jwt.decode(jwt=refresh_token, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
        except Exception as e:
            abort(400)

        username = data.get('username')

        user = db.session.query(User).filter(User.username == username).first()

        data = {
            'username': user.username,
            'role': user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        tokens = {'access_token': access_token, 'refresh_token': refresh_token}

        return tokens
