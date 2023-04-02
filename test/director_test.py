from unittest.mock import MagicMock
import pytest
from dao.director import DirectorDao
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_d = DirectorDao(None)
    Pasha = Director(id=1, name='Pasha')
    Masha = Director(id=2, name='Masha')
    Sasha = Director(id=3, name='Sasha')
    director_d.get_one = MagicMock(return_value=Pasha)
    director_d.get_all = MagicMock(return_value=[Pasha, Masha, Sasha])
    return director_d


class TestDirectorService:

    @pytest.fixture()
    def director_service(self, director_dao):
        director_ser = DirectorService(dao=director_dao)
        return director_ser

    def test_get_one(self, director_service):
        direct = director_service.get_one(1)
        assert direct.name == 'Pasha'

    def test_get_all(self, director_service):
        directs = director_service.get_all()
        assert len(directs) > 0
