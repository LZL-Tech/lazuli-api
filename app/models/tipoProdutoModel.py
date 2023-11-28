from app import db

class TipoProdutoModel(db.Model):
    __tablename__ = 'tipo_produto'
    id: int = db.Column('id_tipo_produto', db.Integer, primary_key=True, autoincrement=True)
    descricao: str = db.Column('descricao', db.String(100))
    produto = db.relationship("ProdutoModel", uselist=False, back_populates="tipo_produto")

    def to_dict(self):
        tipoProduto = {
            'id_tipo_produto': self.id,
            'descricao': self.descricao
        }

        return tipoProduto