from models.produtoModel import ProdutoModel
from repositories.produtoRepository import ProdutoRepository
from repositories.tipoProdutoRepository import TipoProdutoRepository
from repositories.compraRepository import CompraRepository
from repositories.vendaRepository import VendaRepository

class ProdutoService:
    def __init__(self):
        self.produto_repository = ProdutoRepository()
        self.tipo_produto_repository = TipoProdutoRepository()
        self.compra_repository = CompraRepository()
        self.venda_repository = VendaRepository()
        self.listErrors = []

    def find(self, id):
        produtoEncontrado: ProdutoModel = self.produto_repository.find(id)
        if produtoEncontrado is not None:
            return produtoEncontrado.to_dict()           
        return produtoEncontrado

    def findAll(self):
        produtos: list[ProdutoModel] = self.produto_repository.findAll()
        serializados = []

        if len(produtos) > 0:
            for produto in produtos:
                serializados.append(produto.to_dict())

        return serializados

    def create(self, json):
        descricao = json.get('descricao')
        marca = json.get('marca')
        qtd_estoque = json.get('qtd_estoque')
        preco = json.get('preco')
        unidade_medida = json.get('unidadeMedida')
        tipo_produto = json.get('tipoProduto')

        novo_produto = ProdutoModel()

        tipoProdutoEncontrado: ProdutoModel = self.tipo_produto_repository.find(tipo_produto['idTipoProduto'])
        if tipoProdutoEncontrado is not None:
            if tipoProdutoEncontrado.descricao.upper() == 'INGREDIENTE':
                novo_produto.descricao = descricao
                novo_produto.qtd_estoque = qtd_estoque
                novo_produto.id_unidade_medida = unidade_medida['idUnidadeMedida']
                novo_produto.id_tipo_produto = tipo_produto['idTipoProduto']
                novo_produto.marca = marca
            else:
                novo_produto.descricao = descricao
                novo_produto.qtd_estoque = qtd_estoque
                novo_produto.id_unidade_medida = unidade_medida['idUnidadeMedida']
                novo_produto.id_tipo_produto = tipo_produto['idTipoProduto']
                novo_produto.preco = preco

            result = self.produto_repository.create(novo_produto)
            return result
        else:
            return None

    def update(self, id, json):
        produto_encontrado: ProdutoModel = self.produto_repository.find(id)

        descricao = json.get('descricao')
        marca = json.get('marca')
        qtd_estoque = json.get('qtd_estoque')
        preco = json.get('preco')
        unidade_medida = json.get('unidade_medida')
        tipo_produto = json.get('tipo_produto')

        tipoProdutoEncontrado: ProdutoModel = self.tipo_produto_repository.find(tipo_produto['id_tipo_produto'])
        if tipoProdutoEncontrado is not None:
            if tipoProdutoEncontrado.descricao.upper() == 'INGREDIENTE':
                produto_encontrado.descricao = descricao
                produto_encontrado.qtd_estoque = qtd_estoque
                produto_encontrado.id_unidade_medida = unidade_medida['id_unidade_medida']
                produto_encontrado.id_tipo_produto = tipo_produto['id_tipo_produto']
                produto_encontrado.marca = marca
                produto_encontrado.preco = None
            else:
                produto_encontrado.descricao = descricao
                produto_encontrado.qtd_estoque = qtd_estoque
                produto_encontrado.id_unidade_medida = unidade_medida['id_unidade_medida']
                produto_encontrado.id_tipo_produto = tipo_produto['id_tipo_produto']
                produto_encontrado.marca = None
                produto_encontrado.preco = preco

        return self.produto_repository.update(id, produto_encontrado)

    def destroy(self, id):
        if self.compra_repository.checkAssociatedProduct(id) == True:
            self.listErrors.append("Não é possível excluir o produto, pois está associado a compra.")
            return False

        if self.venda_repository.checkAssociatedProduct(id) == True:
            self.listErrors.append("Não é possível excluir o produto, pois está associado a venda.")
            return False     

        return self.produto_repository.destroy(id)

    def findAllSearch(self, args):
        id_tipo = args.get('id_tipo')
        descricao = args.get('descricao')
        serializados = []

        produtos: list[ProdutoModel] = self.produto_repository.findAllSearch(id_tipo, descricao)
        if len(produtos) > 0:
            for produto in produtos:
                serializados.append(produto.to_dict())

        return serializados
    
    def get_all_errors(self):
        return self.listErrors
