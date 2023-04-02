from flask import request
from flask_restx import Namespace, Resource
from implemented import auth_service, user_service

auth_namespace = Namespace("auth")


@auth_namespace.route("/login/")
class AuthsViews(Resource):

    def create(self):
        data = request.json
        if None in [data.get("email", None), data.get("password", None)]:
            return "", 400
        tokens = auth_service.generate_token(data.get("email", None), data.get("password", None))

        return tokens, 201

    def get(self):
        data = request.json
        token = data.get("refresh_token")

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201


@auth_namespace.route("/register/")
class AuthViews(Resource):

    def create(self):
        data = request.json
        user_service.create(data)
        return "", 201
