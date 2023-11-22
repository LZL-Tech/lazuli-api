from app import db
import datetime

class CompraModel(db.Model):
    __tablename__ = 'compra'
    id: int = db.Column('id_compra', db.Integer, primary_key=True, autoincrement=True)
    fornecedor: str = db.Column('fornecedor', db.String(255))
    dt_compra: datetime = db.Column('dt_compra', db.DateTime)