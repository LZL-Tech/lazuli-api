from app import db

class Produto(db.Model):
    __tablename__ = 'Produtos'
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column('Descricao', db.String(255), nullable=False)
    quantidade = db.Column('Quantidade', db.Integer, nullable=False)

    def __init__(self, descricao, quantidade):
        self.descricao = descricao
        self.quantidade = quantidade

    def __repr__(self):
        return '<Descricao %r>' % self.descricao