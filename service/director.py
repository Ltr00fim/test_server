from dao.model.director import Director


class DirectorService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, pk):
        return self.dao.get_one(pk)
