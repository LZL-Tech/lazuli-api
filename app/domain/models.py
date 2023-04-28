from app import db
from datetime import datetime
import decimal


class UnidadeMedida(db.Model):
    __tablename__ = 'unidade_medida'
    id: int = db.Column('id_unidade_medida', db.Integer, primary_key=True, autoincrement=True)
    descricao: str = db.Column('descricao', db.String(100))
    simbolo: str = db.Column('simbolo', db.String(10))


class TipoProduto(db.Model):
    __tablename__ = 'tipo_produto'
    id: int = db.Column('id_tipo_produto', db.Integer, primary_key=True, autoincrement=True)
    descricao: str = db.Column('descricao', db.String(100))


class Produto(db.Model):
    __tablename__ = 'produto'
    id: int = db.Column('id_produto', db.Integer, primary_key=True, autoincrement=True)
    descricao: str = db.Column('descricao', db.String(150), nullable=False)
    marca: str = db.Column('marca', db.String(100), nullable=False)
    qtd_estoque: decimal = db.Column('qtd_estoque', db.Numeric(precision=8, scale=2), nullable=True)
    preco: decimal = db.Column('preco', db.Numeric(precision=8, scale=2), nullable=False)
    id_unidade_medida: int = db.Column(db.Integer, db.ForeignKey('unidade_medida.id_unidade_medida'), nullable=False)
    id_tipo_produto: int = db.Column(db.Integer, db.ForeignKey('tipo_produto.id_tipo_produto'), nullable=False)
    tipo_produto: TipoProduto  = db.relationship(TipoProduto)
    unidade_medida: UnidadeMedida = db.relationship(UnidadeMedida)

    def __repr__(self):
        return '<Descricao %r>' % self.descricao

    def __str__(self) -> str:
        return f'ID: {self.id}, Descricao: {self.descricao}, Qtd_estoque: {self.qtd_estoque}, Tipo de Produto: {self.id_tipo_produto}'


class Compra(db.Model):
    __tablename__ = 'compra'
    id: int = db.Column('id_compra', db.Integer, primary_key=True, autoincrement=True)
    fornecedor: str = db.Column('fornecedor', db.String(255))
    dt_compra: datetime = db.Column('dt_compra', db.DateTime)


class CompraProduto(db.Model):
    __tablename__ = 'compra_produto'
    id: int = db.Column('id_compra_produto', db.Integer, primary_key=True, autoincrement=True)
    id_compra: int = db.Column(db.Integer, db.ForeignKey('compra.id_compra'), nullable=False)
    id_produto: int = db.Column(db.Integer, db.ForeignKey('produto.id_produto'), nullable=False)
    quantidade: decimal = db.Column('quantidade', db.Numeric(precision=8, scale=2), nullable=False)
    vl_unidade: decimal = db.Column('vl_unidade', db.Numeric(precision=8, scale=2), nullable=False)
    vl_total: decimal = db.Column('vl_total', db.Numeric(precision=8, scale=2), nullable=False)
    compra: Compra  = db.relationship(Compra)
    produto: Produto = db.relationship(Produto)