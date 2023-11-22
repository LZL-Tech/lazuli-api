from app import db

class TipoProduto(db.Model):
    __tablename__ = 'tipo_produto'
    id: int = db.Column('id_tipo_produto', db.Integer, primary_key=True, autoincrement=True)
    descricao: str = db.Column('descricao', db.String(100))