from app import db

from models.compraProdutoModel import CompraProdutoModel
from models.produtoModel import ProdutoModel
from models.compraModel import CompraModel
from repositories.baseRepository import BaseRepository


class CompraRepository(BaseRepository):
    def __init__(self):
        super().__init__(CompraModel)

    def find(self, id):
        item = db.session.query(CompraModel, CompraProdutoModel, ProdutoModel).join(
                CompraProdutoModel, CompraProdutoModel.id_compra == CompraModel.id).join(
                ProdutoModel, ProdutoModel.id == CompraProdutoModel.id_produto
            ).filter(CompraModel.id == id).first()
        return item

    def findAll(self):
        list = db.session.query(CompraModel, CompraProdutoModel, ProdutoModel).join(
                CompraProdutoModel, CompraProdutoModel.id_compra == CompraModel.id).join(
                ProdutoModel, ProdutoModel.id == CompraProdutoModel.id_produto
            ).all()
        return list

    def checkAssociatedProduct(self, id_produto):
        result = False

        item = db.session.query(CompraModel, CompraProdutoModel, ProdutoModel).join(
                CompraProdutoModel, CompraProdutoModel.id_compra == CompraModel.id).join(
                ProdutoModel, ProdutoModel.id == CompraProdutoModel.id_produto
            ).filter(ProdutoModel.id == id_produto).first()

        if item is not None:
            result = True

        return result

    def searchCompraProductId(self, id_produto):
        list = db.session.query(CompraModel, CompraProdutoModel, ProdutoModel).join(
                CompraProdutoModel, CompraProdutoModel.id_compra == CompraModel.id).join(
                ProdutoModel, ProdutoModel.id == CompraProdutoModel.id_produto
            ).filter(ProdutoModel.id == id_produto).all()
        return list