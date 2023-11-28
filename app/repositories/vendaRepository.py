from app import db

from models.vendaModel import VendaModel
from models.produtoModel import ProdutoModel
from models.vendaProdutoModel import VendaProdutoModel
from repositories.baseRepository import BaseRepository


class VendaRepository(BaseRepository):
    def __init__(self):
        super().__init__(VendaModel)

    def find(self, id):
        item = db.session.query(VendaModel, VendaProdutoModel, ProdutoModel).join(
                VendaProdutoModel, VendaProdutoModel.id_venda == VendaModel.id).join(
                ProdutoModel, ProdutoModel.id == VendaProdutoModel.id_produto
            ).filter(VendaModel.id == id).first()
        return item

    def findAll(self):
        list = db.session.query(VendaModel, VendaProdutoModel, ProdutoModel).join(
                VendaProdutoModel, VendaProdutoModel.id_venda == VendaModel.id).join(
                ProdutoModel, ProdutoModel.id == VendaProdutoModel.id_produto
            ).all()
        return list

    def checkAssociatedProduct(self, id_produto):
        result = False

        item = db.session.query(VendaModel, VendaProdutoModel, ProdutoModel).join(
                VendaProdutoModel, VendaProdutoModel.id_venda == VendaModel.id).join(
                ProdutoModel, ProdutoModel.id == VendaProdutoModel.id_produto
            ).filter(ProdutoModel.id == id_produto).first()

        if item is not None:
            result = True

        return result

    def searchVendaProductId(self, id_produto):
        list = db.session.query(VendaModel, VendaProdutoModel, ProdutoModel).join(
                VendaProdutoModel, VendaProdutoModel.id_venda == VendaModel.id).join(
                ProdutoModel, ProdutoModel.id == VendaProdutoModel.id_produto
            ).filter(ProdutoModel.id == id_produto).all()
        return list