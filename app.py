from flask import Flask, render_template
from flask_restx import Api
from config import Config
from setup_db import db
from views.auth import auth_namespace
from views.director import director_namespace
from views.genre import genre_namespace
from views.movie import movie_namespace
from views.user import user_namespace


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)

    return app


def register_extensions(app):
    @app.route("/")
    def index():
        return render_template("index.html")
    db.init_app(app)
    api = Api(app, title="Flask Course Project 3", doc="/docs")
    api.add_namespace(director_namespace)
    api.add_namespace(genre_namespace)
    api.add_namespace(movie_namespace)
    api.add_namespace(auth_namespace)
    api.add_namespace(user_namespace)


app = create_app(Config)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=10001)
