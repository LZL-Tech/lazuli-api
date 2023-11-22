from app import db
import logging as log

from interfaces.irepository import IRepository


class BaseRepository(IRepository):
    def __init__(self, classe):
        self.classe = classe

    def find(self, id):
        item = self.classe.query.get(id)
        return item

    def findAll(self):
        list = self.classe.query.order_by(self.classe.id).all()
        return list

    def create(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as ex:
            log.error(ex)
            db.session.rollback()
            return None

    def update(self, id, obj):       
        item = self.classe.query.get(id)
        if item is not None:
            try:
                for key, value in obj.__dict__.items():
                    if key != '_sa_instance_state':
                        setattr(item, key, value)
                db.session.commit()
                return True
            except Exception as ex:
                log.error(ex)
                db.session.rollback()
                return False
        return False

    def destroy(self, id):
        item = self.classe.query.get(id)
        if item is not None:
            try:
                db.session.delete(item)
                db.session.commit()
                return True
            except Exception as ex:
                log.error(ex)
                db.session.rollback()
                return False
        return False