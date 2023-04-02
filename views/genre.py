from flask import request
from flask_restx import Namespace, Resource
from implemented import genre_service
from dao.model.genre import GenreSchema
from decorators import auth_required

genre_namespace = Namespace("genre")

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_namespace.route("/")
class GenresView(Resource):
    @auth_required
    def get(self):
        genres = genre_service.get_all()
        return genres_schema.dump(genres), 200

    @auth_required
    def post(self):
        data = request.json
        genre_service.create(data)
        return "", 201


@genre_namespace.route("/<pk>/")
class GenreView(Resource):
    @auth_required
    def get(self, pk):
        genre = genre_service.get_one(int(pk))
        return genre_schema.dump(genre), 200

    @auth_required
    def put(self, pk):
        data = request.json
        genre_service.update(data, int(pk))
        return "", 204

    @auth_required
    def delete(self, pk):
        genre_service.delete(int(pk))
        return "", 204
