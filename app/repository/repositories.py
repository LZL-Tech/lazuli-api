from app import db, joinedload
from repository.interfaces import IRepository
from domain.models import *
import logging as log

class RepositoryBase(IRepository):
    def __init__(self, classe):
        self.classe = classe

    def find(self, id):
        item = self.classe.query.get(id)
        return item

    def findAll(self):
        list = self.classe.query.order_by(self.classe.id).all()
        return list

    def create(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as ex:
            log.error(ex)
            db.session.rollback()
            return None

    def update(self, id, obj):
        item = self.find(id)
        if item is not None:
            for key, value in obj.__dict__.items():
                if key != '_sa_instance_state':
                    setattr(item, key, value)
            db.session.commit()
            return True
        return False

    def destroy(self, id):
        item = self.find(id)
        if item is not None:
            try:
                db.session.delete(item)
                db.session.commit()
                return True
            except Exception as ex:
                log.error(ex)
                return False
        return False

class ProdutoRepository(RepositoryBase):
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

class TipoProdutoRepository(RepositoryBase):
    def __init__(self):
        super().__init__(TipoProduto)


    def findByDescricao(descricao: str):
        try:
            tipo_produto: TipoProduto = db.session.query(TipoProduto).filter_by(descricao=descricao)
            return tipo_produto
        except Exception as ex:
            log.error(ex)
            return None

class UnidadeMedidaRepository(RepositoryBase):

    def __init__(self):
        super().__init__(UnidadeMedida)

class CompraRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Compra)

    def find(self, id):
        item = db.session.query(Compra, CompraProduto, Produto).join(
                CompraProduto, CompraProduto.id_compra == Compra.id).join(
                Produto, Produto.id == CompraProduto.id_produto
            ).filter(Compra.id == id).all()

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

class CompraProdutoRepository(RepositoryBase):

    def __init__(self):
        super().__init__(CompraProduto)

class VendaRepository(RepositoryBase):

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


class VendaProdutoRepository(RepositoryBase):

    def __init__(self):
        super().__init__(VendaProduto)

    def findByVendaId(self, id):
        try:
            venda_produto: VendaProduto = db.session.query(VendaProduto).filter_by(id_venda=id)
            return venda_produto
        except Exception as ex:
            log.error(ex)
            return None