from app import db
from typing import List
import logging as log

from models.vendaProdutoModel import VendaProdutoModel

from repositories.baseRepository import BaseRepository


class VendaProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__(VendaProdutoModel)

    def findByVendaId(self, id):
        try:
            list_venda_produto: List[VendaProdutoModel] = (db.session.query(VendaProdutoModel)
                                                      .filter_by(id_venda=id)
                                                      .all())
            if list_venda_produto:
                return list_venda_produto

            return None
        except Exception as ex:
            log.error(ex)
            return None
        
    def destroyByVendaId(self, id):
        try:
            itens: List[VendaProdutoModel] = (db.session.query(VendaProdutoModel)
                                         .filter_by(id_venda=id)
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