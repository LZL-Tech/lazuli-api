from app import db
from sqlalchemy.orm import joinedload

from models.unidadeMedida import UnidadeMedida
from models.tipoProduto import TipoProduto
from models.produto import Produto
from repositories.baseRepository import BaseRepository


class ProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Produto)

    def findAll(self):
        list = db.session.query(Produto).options(
            joinedload('unidade_medida'),
            joinedload('tipo_produto')
        ).all()
        return list

    def findAllSearch(self, id_tipo, descricao):
        list = db.session.query(Produto).join(TipoProduto).join(
            UnidadeMedida, Produto.unidade_medida).filter(
                Produto.descricao.like(f"%{descricao}%"),
                TipoProduto.id == id_tipo
            ).options(
                joinedload('unidade_medida'),
                joinedload('tipo_produto')
            ).all()
        return list