from domain.tipo_produto import TipoProduto
from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app import db


class Produto(db.Model):
    __tablename__ = 'produto'
    id = Column('id_produto', Integer, primary_key=True, autoincrement=True)
    descricao = Column('descricao', String(150), nullable=False)
    quantidade = Column('qtd_estoque', Float, nullable=True)
    id_tipo_produto = Column(Integer, ForeignKey('tipo_produto.id_tipo_produto'))


    def __repr__(self):
        return '<Descricao %r>' % self.descricao
    
    def __str__(self) -> str:
        return f'ID: {self.id}, Descricao: {self.descricao}, Quantidade: {self.quantidade}, Tipo de Produto: {self.id_tipo_produto}'