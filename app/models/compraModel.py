from app import db
import datetime

class CompraModel(db.Model):
    __tablename__ = 'compra'
    id: int = db.Column('id_compra', db.Integer, primary_key=True, autoincrement=True)
    fornecedor: str = db.Column('fornecedor', db.String(255), nullable=False)
    dt_compra: datetime = db.Column('dt_compra', db.DateTime)
    compraProdutos = db.relationship('CompraProdutoModel', back_populates='compra')

    def to_dict(self):
        compra = {
            "id_compra": self.id,
            "fornecedor": self.fornecedor,
            "dt_compra": self.dt_compra.strftime('%Y-%m-%d'),
            "venda_produto": [cp.to_dict() for cp in self.compraProdutos]
        }

        return compra