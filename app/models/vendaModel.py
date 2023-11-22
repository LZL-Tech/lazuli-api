from app import db
from datetime import datetime

class VendaModel(db.Model):
    __tablename__='venda'
    id: int = db.Column('id_venda', db.Integer, primary_key=True, autoincrement=True)
    nm_cliente: str = db.Column('nm_cliente', db.String(255), nullable=True)
    dt_venda: datetime = db.Column('dt_venda', db.DateTime, nullable=True)
    vendaProdutos = db.relationship("VendaProdutoModel", back_populates="venda")