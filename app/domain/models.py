from app import db
import decimal

class UnidadeMedida(db.Model):
    __tablename__ = 'unidade_medida'
    id: int = db.Column('id_unidade_medida', db.Integer, primary_key=True, autoincrement=True)
    descricao: str = db.Column('descricao', db.String(100))
    simbolo: str = db.Column('simbolo', db.String(10))


class TipoProduto(db.Model):
    __tablename__ = 'tipo_produto'
    id: int = db.Column('id_tipo_produto', db.Integer, primary_key=True, autoincrement=True)
    descricao: str = db.Column('descricao', db.String(100))


class Produto(db.Model):
    __tablename__ = 'produto'
    id: int = db.Column('id_produto', db.Integer, primary_key=True, autoincrement=True)
    descricao: str = db.Column('descricao', db.String(150), nullable=False)
    marca: str = db.Column('marca', db.String(100), nullable=False)
    qtd_estoque: float = db.Column('qtd_estoque', db.Numeric(precision=8, scale=2), nullable=True)
    preco: float = db.Column('preco', db.Numeric(precision=8, scale=2), nullable=False)
    id_unidade_medida: int = db.Column(db.Integer, db.ForeignKey('unidade_medida.id_unidade_medida'), nullable=False)
    id_tipo_produto: int = db.Column(db.Integer, db.ForeignKey('tipo_produto.id_tipo_produto'), nullable=False)
    tipo_produto: TipoProduto  = db.relationship(TipoProduto)
    unidade_medida: UnidadeMedida = db.relationship(UnidadeMedida)

    def __repr__(self):
        return '<Descricao %r>' % self.descricao

    def __str__(self) -> str:
        return f'ID: {self.id}, Descricao: {self.descricao}, Qtd_estoque: {self.qtd_estoque}, Tipo de Produto: {self.id_tipo_produto}'
