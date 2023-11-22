from app import db
import decimal

from models.tipoProduto import TipoProduto
from models.unidadeMedida import UnidadeMedida

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
    vendaProdutos = db.relationship("VendaProduto", back_populates="produto")