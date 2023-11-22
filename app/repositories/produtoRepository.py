from app import db
from sqlalchemy.orm import joinedload

from models.unidadeMedidaModel import UnidadeMedidaModel
from models.tipoProdutoModel import TipoProdutoModel
from models.produtoModel import ProdutoModel

from repositories.baseRepository import BaseRepository


class ProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProdutoModel)

    def findAll(self):
        list = db.session.query(ProdutoModel).options(
            joinedload('unidade_medida'),
            joinedload('tipo_produto')
        ).all()
        return list

    def findAllSearch(self, id_tipo, descricao):
        list = db.session.query(ProdutoModel).join(TipoProdutoModel).join(
            UnidadeMedidaModel, ProdutoModel.unidade_medida).filter(
                ProdutoModel.descricao.like(f"%{descricao}%"),
                TipoProdutoModel.id == id_tipo
            ).options(
                joinedload('unidade_medida'),
                joinedload('tipo_produto')
            ).all()
        return list