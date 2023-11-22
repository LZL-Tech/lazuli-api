from app import db
import logging as log

from repositories.baseRepository import BaseRepository
from models.tipoProdutoModel import TipoProdutoModel


class TipoProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__(TipoProdutoModel)

    def findByDescricao(descricao: str):
        try:
            tipo_produto: TipoProdutoModel = (db.session.query(TipoProdutoModel)
                                         .filter_by(descricao=descricao)
                                         .first())
            return tipo_produto
        except Exception as ex:
            log.error(ex)
            return None