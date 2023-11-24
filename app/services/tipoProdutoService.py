from typing import List
from models.tipoProdutoModel import TipoProdutoModel
from repositories.tipoProdutoRepository import TipoProdutoRepository

class TipoProdutoService:
    def __init__(self):
        self.tipo_produto_repository = TipoProdutoRepository()
        self.listErrors = []

    def findAll(self):
        tipo_produtos: List[TipoProdutoModel] = self.tipo_produto_repository.findAll()
        serializados = []

        if len(tipo_produtos) > 0:
            for tipo_produto in tipo_produtos:
                serializados.append(tipo_produto.to_dict())
        
        return serializados

    def get_all_errors(self):
        return self.listErrors
