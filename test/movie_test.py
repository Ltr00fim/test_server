from unittest.mock import MagicMock
import pytest
from dao.movie import MovieDao
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDao(None)
    movie1 = Movie(id=1, title='title1', description='description1', trailer='trailer1', year=2023, rating=5, genre_id=1, director_id=1)
    movie2 = Movie(id=2, title='title2', description='description2', trailer='trailer2', year=2022, rating=4, genre_id=2, director_id=2)
    movie3 = Movie(id=3, title='title3', description='description3', trailer='trailer3', year=2021, rating=3, genre_id=3, director_id=3)
    movie_dao.get_one = MagicMock(return_value=movie1)
    movie_dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    movie_dao.delete = MagicMock(return_value='')
    movie_dao.create = MagicMock(return_value='')
    movie_dao.update = MagicMock(return_value='')
    movie_dao.get_by_director_id = MagicMock(return_value=movie1)
    movie_dao.get_by_year = MagicMock(return_value=movie2)
    movie_dao.get_by_genre_id = MagicMock(return_value=movie3)
    return movie_dao


class TestsMovieService:

    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        movie_ser = MovieService(dao=movie_dao)
        return movie_ser

    def test_get_one(self, movie_service):
        movie = movie_service.get_one(1)
        assert movie.title == 'title1'

    def test_get_all(self, movie_service):
        movies = movie_service.get_all('')
        assert movies[1].title == 'title2'

    def test_delete(self, movie_service):
        movie = movie_service.delete(9)
        assert movie is None

    def test_create(self, movie_service):
        movie = movie_service.create(8)
        assert movie is not None

    def test_update(self, movie_service):
        movie = movie_service.update(4)
        assert movie is not None
