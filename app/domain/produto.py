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
    
class Compra(db.Model):
    __tablename__ = 'compra'
    id_compra: int = db.Column('id_compra', db.Integer, primary_key=True, autoincrement=True)
    Fornecedor: str = db.Column('fornecedor', db.String(255), nullable=False)
    dt_Compra: datetime = db.Column('dt_Compra', db.DateTime, default =datetime.utcnow)

class CompraProduto(db.Model):
    __tablename__ = 'compra_produto'
    id_compra_produto: int = db.Column('id_compra_produto', db.Integer, primary_key=True, autoincrement=True)
    id_compra: int = db.Column('id_compra', db.Integer, foreign_key=True, autoincrement=True)
    id_produto: int = db.Column('id_produto', db.Integer, foreign_key=True, autoincrement=True)
    quantidade: int = db.Column('quantidade', db.Integer, nullable=True)
    vl_unidade: float = db.Column('vl_unidade', db.Float, nullable=True)
    vl_total: float = db.Column('vl_total', db.Float, nullable=True)
