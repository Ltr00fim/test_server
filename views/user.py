from flask_restx import Namespace, Resource
from implemented import user_service
from dao.model.user import UserSchema
from flask import request

user_namespace = Namespace("user")

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_namespace.route("/")
class UsersView(Resource):
    def get(self):
        users = user_service.get_all()
        return users_schema.dump(users), 200

    def post(self):
        data = request.json
        user_service.create(data)
        return "", 201


@user_namespace.route("/<pk>")
class UserViews(Resource):
    def get(self, pk):
        user = user_service.get_one(int(pk))
        return user_schema.dump(user), 200

    def put(self):
        data = request.json
        user_service.update(data)
        return "", 204

    def patch(self, pk):
        data = request.json
        user_service.update_partial(data, int(pk))
        return "", 204


@user_namespace.route("/password/<pk>")
class UserView(Resource):

    def put(self, pk):
        data = request.json
        user_service.update_partial(data, int(pk))
        return "", 204
