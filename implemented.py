from setup_db import db

from dao.movie import MovieDao
from service.movie import MovieService

from dao.director import DirectorDao
from service.director import DirectorService

from dao.genre import GenreDao
from service.genre import GenreService

from dao.user import UserDao
from service.user import UserService

from service.auth import AuthService

movie_dao = MovieDao(db.session)
genre_dao = GenreDao(db.session)
director_dao = DirectorDao(db.session)
user_dao = UserDao(db.session)

movie_service = MovieService(dao=movie_dao)
genre_service = GenreService(dao=genre_dao)
director_service = DirectorService(dao=director_dao)
user_service = UserService(dao=user_dao)
auth_service = AuthService(user_service)
