from app import db
import decimal

from models.vendaModel import VendaModel
from models.produtoModel import ProdutoModel

class VendaProdutoModel(db.Model):
    __tablename__ = 'venda_produto'
    id: int = db.Column('id_venda_produto', db.Integer, primary_key=True, autoincrement=True)
    quantidade: decimal = db.Column('quantidade', db.Numeric(precision=8, scale=2), nullable=True)
    preco_unidade: decimal = db.Column('preco_unidade', db.Numeric(precision=8, scale=2), nullable=False)
    id_produto: int = db.Column(db.Integer, db.ForeignKey('produto.id_produto'), nullable=False)
    id_venda: int = db.Column(db.Integer, db.ForeignKey('venda.id_venda'), nullable=False)
    venda: VendaModel = db.relationship("VendaModel", back_populates="vendaProdutos")
    produto: ProdutoModel = db.relationship("ProdutoModel", back_populates="vendaProdutos")

    def to_dict(self):
        vendaProduto = {
            "id_venda_produto": self.id,
            "quantidade": self.quantidade,
            "preco_unidade": self.preco_unidade,
            "id_produto": self.id_produto,
            "id_venda": self.id_venda,
            'produto': self.produto.to_dict()
        }

        return vendaProduto