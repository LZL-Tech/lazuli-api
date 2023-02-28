from app import db
from repository.abstract_repository import IRepository
from domain.produto import Produto

class RepositoryBase(IRepository):
    def __init__(self, classe):
        self.classe = classe

    def find(self, id):
        item = self.classe.query.get(id)
        return item

    def findAll(self):
        list = self.classe.query.order_by(self.classe.id)
        return list

    def create(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def update(self, id, obj):
        item = self.find(id)
        if item is not None:
            for key, value in obj.__dict__.items():
                if key != '_sa_instance_state':
                    setattr(item, key, value)
            db.session.commit()
            return True
        return False

    def destroy(self, id):
        item = self.find(id)
        if item is not None:
            try:
                db.session.delete(item)
                db.session.commit()
                return True
            except:
                return False
        return False

class ProdutoRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Produto)