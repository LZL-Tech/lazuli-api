from app import db

from models.compraProduto import CompraProduto
from models.produto import Produto
from models.compra import Compra
from repositories.baseRepository import BaseRepository


class CompraRepository(BaseRepository):
    def __init__(self):
        super().__init__(Compra)

    def find(self, id):
        item = db.session.query(Compra, CompraProduto, Produto).join(
                CompraProduto, CompraProduto.id_compra == Compra.id).join(
                Produto, Produto.id == CompraProduto.id_produto
            ).filter(Compra.id == id).first()
        return item

    def findAll(self):
        list = db.session.query(Compra, CompraProduto, Produto).join(
                CompraProduto, CompraProduto.id_compra == Compra.id).join(
                Produto, Produto.id == CompraProduto.id_produto
            ).all()
        return list

    def checkAssociatedProduct(self, id_produto):
        result = False

        item = db.session.query(Compra, CompraProduto, Produto).join(
                CompraProduto, CompraProduto.id_compra == Compra.id).join(
                Produto, Produto.id == CompraProduto.id_produto
            ).filter(Produto.id == id_produto).first()

        if item is not None:
            result = True

        return result

    def searchCompraProductId(self, id_produto):
        list = db.session.query(Compra, CompraProduto, Produto).join(
                CompraProduto, CompraProduto.id_compra == Compra.id).join(
                Produto, Produto.id == CompraProduto.id_produto
            ).filter(Produto.id == id_produto).all()
        return list