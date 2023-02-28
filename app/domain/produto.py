from app import db
from sqlalchemy import String, Integer, Float, ForeignKey, Column

class Produto(db.Model):
    __tablename__ = 'produto'
    id = Column('id_produto', Integer, primary_key=True, autoincrement=True)
    descricao = Column('descricao', String(150), nullable=False)
    quantidade = Column('qtd_estoque', Float, nullable=True)
    tipo_produto = Column('id_tipo_produto', Integer, ForeignKey('tipo_produto.id_tipo_produto'))


    def __init__(self, descricao, quantidade):
        self.descricao = descricao
        self.quantidade = quantidade

    def __repr__(self):
        return '<Descricao %r>' % self.descricao