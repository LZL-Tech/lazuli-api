from app import db
from datetime import datetime

class VendaModel(db.Model):
    __tablename__='venda'
    id: int = db.Column('id_venda', db.Integer, primary_key=True, autoincrement=True)
    nm_cliente: str = db.Column('nm_cliente', db.String(255), nullable=True)
    dt_venda: datetime = db.Column('dt_venda', db.DateTime, nullable=True)
    vendaProdutos = db.relationship("VendaProdutoModel", back_populates="venda")

    def to_dict(self):
        venda = {
            "id_venda": self.id,
            "nm_cliente": self.nm_cliente,
            "dt_venda": self.dt_venda.strftime('%Y-%m-%d'),
            "venda_produto": [vp.to_dict() for vp in self.vendaProdutos]
        }

        return venda