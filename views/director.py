from flask import request
from flask_restx import Namespace, Resource
from implemented import director_service
from dao.model.director import DirectorSchema
from decorators import auth_required

director_namespace = Namespace("directors")

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_namespace.route("/")
class DirectorsView(Resource):
    @auth_required
    def get(self):
        directors = director_service.get_all()
        return directors_schema.dump(directors), 200

    @auth_required
    def post(self):
        data = request.json
        director_service.create(data)
        return "", 201


@director_namespace.route("/<pk>/")
class DirectorView(Resource):
    @auth_required
    def get(self, pk):
        director = director_service.get_one(int(pk))
        return director_schema.dump(director), 200

    @auth_required
    def put(self, pk):
        data = request.json
        director_service.update(data, int(pk))
        return "", 204

    @auth_required
    def delete(self, pk):
        director_service.delete(int(pk))
        return "", 204
