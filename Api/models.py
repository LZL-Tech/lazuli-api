from app import db

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column('id_produto', db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column('descricao', db.String(150), nullable=False)
    marca = db.Column('marca', db.String(100), nullable=False)
    qtd_estoque = db.Column('qtd_estoque', db.Float, nullable=True)
    preco = db.Column('preco', db.Numeric(precision=8, scale=2), nullable=False)
    id_unidade_medida = db.Column(db.Integer, db.ForeignKey('unidade_medida.id_unidade_medida'), nullable=False)
    id_tipo_produto = db.Column(db.Integer, db.ForeignKey('tipo_produto.id_tipo_produto'), nullable=False)

    def __repr__(self):
        return '<Descricao %r>' % self.descricao
    
    def __str__(self) -> str:
        return f'ID: {self.id}, Descricao: {self.descricao}, Qtd_estoque: {self.qtd_estoque}, Tipo de Produto: {self.id_tipo_produto}'


class UnidadeMedida(db.Model):
    __tablename__ = 'unidade_medida'

    id = db.Column('id_unidade_medida', db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column('descricao', db.String(100))
    simbolo = db.Column('simbolo', db.String(10))
    produto = db.relationship('Produto', backref='unidade_medida', lazy=True)


class TipoProduto(db.Model):
    __tablename__ = 'tipo_produto'
    id = db.Column('id_tipo_produto', db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column('descricao', db.String(100))
    produto = db.relationship('Produto', backref='tipo_produto', lazy=True)