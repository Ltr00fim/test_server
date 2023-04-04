import calendar
import datetime
import hashlib
import base64
import jwt
from flask import request, abort
from flask_restx import Resource, Namespace
from config import Config
from dao.model.user import User
from implemented import user_service
from setup_db import db

auth_namespace = Namespace('auth')


@auth_namespace.route('/login/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email')
        password = req_json.get('password')

        user = User.query.filter(User.email == email).first()

        if user is None:
            abort(401)

        hash_password = base64.b64encode(
            hashlib.pbkdf2_hmac('sha256',
                                password.encode('utf-8'),
                                Config.PWD_HASH_SALT,
                                Config.PWD_HASH_ITERATIONS
                                ))

        if user.password != hash_password:
            abort(401)

        data = {'email': email,
                'role': user.role
                }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        tokens = {'access_token': access_token,
                  'refresh_token': refresh_token
                  }

        return tokens

    def put(self):

        req_json = request.json
        access_token = req_json.get('access_token')
        refresh_token = req_json.get('refresh_token')

        try:
            data = jwt.decode(access_token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
            data = jwt.decode(refresh_token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])

        except Exception as e:
            print(e)
            abort(401)

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        tokens = {'access_token': access_token,
                  'refresh_token': refresh_token
                  }

        return tokens


@auth_namespace.route('/register')
class AuthsView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email')
        password = req_json.get('password')
        role = req_json.get('role')
        if role is None:
            role = 'user'

        if password is None or email is None or role is None:
            abort(401)

        data = {'password': password,
                'email': email,
                'role': role}

        user_service.create(data)

        data = {'email': email,
                'role': role
                }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        tokens = {'access_token': access_token,
                  'refresh_token': refresh_token
                  }

        return tokens

    def put(self):
        req_json = request.json
        refresh_token = req_json.get('refresh_token')

        if refresh_token is None:
            abort(401)

        try:
            data = jwt.decode(jwt=refresh_token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        except Exception as e:
            print(e)
            abort(400)

        email = data.get('email')

        user = db.session.query(User).filter(User.email == email).first()

        data = {'username': user.username,
                'role': user.role
                }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        tokens = {'access_token': access_token,
                  'refresh_token': refresh_token
                  }

        return tokens
