from app import db

class UnidadeMedidaModel(db.Model):
    __tablename__ = 'unidade_medida'
    id: int = db.Column('id_unidade_medida', db.Integer, primary_key=True, autoincrement=True)
    descricao: str = db.Column('descricao', db.String(100))
    simbolo: str = db.Column('simbolo', db.String(10))