from app import db
from typing import List
import logging as log

from models.compraProdutoModel import CompraProdutoModel
from repositories.baseRepository import BaseRepository


class CompraProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__(CompraProdutoModel)

    def findByCompraId(self, id):
        try:
            list_compra_produto: List[CompraProdutoModel] = (db.session.query(CompraProdutoModel)
                                                        .filter_by(id_compra=id)
                                                        .all())
            if list_compra_produto:
                return list_compra_produto
            else:
                return None
        except Exception as ex:
            log.error(ex)
            return None
        
    def destroyByCompraId(self, id):
        try:
            itens: List[CompraProdutoModel] = (db.session.query(CompraProdutoModel)
                                          .filter_by(id_compra=id)
                                          .all())
            if len(itens) > 0:
                for item_delete in itens:
                    db.session.delete(item_delete)
                    db.session.commit()
                return True
            return False
        except Exception as ex:
            log.error(ex)
            db.session.rollback()         
            return False 