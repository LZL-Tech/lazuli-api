from app import db

from models.venda import Venda
from models.produto import Produto
from models.vendaProduto import VendaProduto
from repositories.baseRepository import BaseRepository


class VendaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Venda)

    def checkAssociatedProduct(self, id_produto):
        result = False

        item = db.session.query(Venda, VendaProduto, Produto).join(
                VendaProduto, VendaProduto.id_venda == Venda.id).join(
                Produto, Produto.id == VendaProduto.id_produto
            ).filter(Produto.id == id_produto).first()

        if item is not None:
            result = True

        return result

    def searchVendaProductId(self, id_produto):
        list = db.session.query(Venda, VendaProduto, Produto).join(
                VendaProduto, VendaProduto.id_venda == Venda.id).join(
                Produto, Produto.id == VendaProduto.id_produto
            ).filter(Produto.id == id_produto).all()
        return list