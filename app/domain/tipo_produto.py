from app import db
from sqlalchemy import Column, String, Integer

class TipoProduto(db.Model):
    __tablename__ = 'tipo_produto'

    id = Column('id_tipo_produto', Integer, primarykey=True, autoincrement=True)
    descricao = Column('descricao', String(100))