from app import db
import logging as log

from repositories.baseRepository import BaseRepository
from models.tipoProduto import TipoProduto


class TipoProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__(TipoProduto)

    def findByDescricao(descricao: str):
        try:
            tipo_produto: TipoProduto = (db.session.query(TipoProduto)
                                         .filter_by(descricao=descricao)
                                         .first())
            return tipo_produto
        except Exception as ex:
            log.error(ex)
            return None