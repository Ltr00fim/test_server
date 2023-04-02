from flask_restx import Namespace, Resource
from implemented import movie_service
from dao.model.movie import MovieSchema
from flask import request
from decorators import auth_required

movie_namespace = Namespace("movies")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_namespace.route("/")
class MoviesView(Resource):
    @auth_required
    def get(self):
        genres_args = request.args.get("genre_id", False)
        director_args = request.args.get("director_id", False)
        year_args = request.args.get("year", False)
        status = request.args.get("status", False)
        page = request.args.get("page", False)
        movie = movie_service.get_all(genres_args, director_args, year_args, status, page)
        return movies_schema.dump(movie), 200

    @auth_required
    def post(self):
        data = request.json
        movie_service.create(data)
        return "", 201


@movie_namespace.route("/<int:pk>/")
class MovieView(Resource):
    @auth_required
    def get(self, pk):
        movie = movie_service.get_one(int(pk))
        return movie_schema.dump(movie), 200

    @auth_required
    def put(self, pk):
        data = request.json
        movie_service.update(data, int(pk))
        return "", 204

    @auth_required
    def delete(self, pk):
        movie_service.delete(int(pk))
        return "", 204
