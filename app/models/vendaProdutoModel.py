from app import db
import decimal

class VendaProdutoModel(db.Model):
    __tablename__ = 'venda_produto'
    id: int = db.Column('id_venda_produto', db.Integer, primary_key=True, autoincrement=True)
    quantidade: decimal = db.Column('quantidade', db.Numeric(precision=8, scale=2), nullable=True)
    preco_unidade: decimal = db.Column('preco_unidade', db.Numeric(precision=8, scale=2), nullable=False)
    id_produto: int = db.Column(db.Integer, db.ForeignKey('produto.id_produto'), nullable=False)
    id_venda: int = db.Column(db.Integer, db.ForeignKey('venda.id_venda'), nullable=False)
    venda = db.relationship("VendaModel", back_populates="vendaProdutos")
    produto = db.relationship("ProdutoModel", back_populates="vendaProdutos")