from app import db
import decimal

from models.compraModel import CompraModel
from models.produtoModel import ProdutoModel

class CompraProdutoModel(db.Model):
    __tablename__ = 'compra_produto'
    id: int = db.Column('id_compra_produto', db.Integer, primary_key=True, autoincrement=True)
    id_compra: int = db.Column(db.Integer, db.ForeignKey('compra.id_compra'), nullable=False)
    id_produto: int = db.Column(db.Integer, db.ForeignKey('produto.id_produto'), nullable=False)
    quantidade: decimal = db.Column('quantidade', db.Numeric(precision=8, scale=2), nullable=False)
    vl_unidade: decimal = db.Column('vl_unidade', db.Numeric(precision=8, scale=2), nullable=False)
    vl_total: decimal = db.Column('vl_total', db.Numeric(precision=8, scale=2), nullable=False)
    produto: ProdutoModel = db.relationship("ProdutoModel", back_populates="compraProdutos")
    compra: CompraModel = db.relationship("CompraModel", back_populates="compraProdutos")

    def to_dict(self):
        compraProduto = {
            "id_compra_produto": self.id,
            "id_compra": self.id_compra,
            "id_produto": self.id_produto,
            "quantidade": self.quantidade,
            "vl_unidade": self.vl_unidade,
            "vl_total": self.vl_total,
            "produto": self.produto.to_dict()
        }

        return compraProduto