from models.vendaModel import VendaModel
from models.vendaProdutoModel import VendaProdutoModel
from repositories.vendaProdutoRepository import VendaProdutoRepository
from repositories.vendaRepository import VendaRepository


class VendaService:
    def __init__(self):
        self.venda_repository = VendaRepository()
        self.venda_produto_repository = VendaProdutoRepository()
        self.listErrors = []

    def find(self, id):
        v, vp, p = self.venda_repository.find(id)
        if v is not None:
            return v.to_dict()     
        return v

    def findAll(self):
        vendas = self.venda_repository.findAll()
        serializados = []

        if len(vendas) > 0:
            for v, vp, p in vendas:
                serializados.append(v.to_dict())

        return serializados

    # def create(self, json):
    #     fornecedor = json.get('fornecedor')
    #     dt_compra = json.get('dt_compra')
    #     compra_produto = json.get('compra_produto')

    #     if not fornecedor or not dt_compra or not compra_produto:
    #         self.listErrors.append("Dados incompletos.") # 400
    #         return None
        
    #     for item in compra_produto:
    #         quantidade = item['quantidade']

    #         if not quantidade:
    #             self.listErrors.append("O campo 'quantidade' é obrigatório.") # 400
    #             return result_compra
            
    #     nova_compra = CompraModel()
    #     nova_compra.fornecedor = fornecedor
    #     nova_compra.dt_compra = dt_compra

    #     result_compra: CompraModel = self.compra_repository.create(nova_compra)
    #     if result_compra is None:
    #         self.listErrors.append("Erro ao cadastrar compra") # 500
    #         return result_compra

    #     for item in compra_produto:
    #         id_produto = item['produto']['id_produto']
    #         quantidade = item['quantidade']
    #         vl_unidade = item['vl_unidade']
    #         vl_total = item['vl_total']

    #         if vl_total is not None and vl_unidade is None:
    #             vl_unidade = vl_total / quantidade

    #         if vl_unidade is not None and vl_total is None:
    #             vl_total = vl_unidade * quantidade

    #         nova_compra_produto = CompraProdutoModel()
    #         nova_compra_produto.id_compra = result_compra.id
    #         nova_compra_produto.id_produto = id_produto
    #         nova_compra_produto.quantidade = quantidade
    #         nova_compra_produto.vl_unidade = vl_unidade
    #         nova_compra_produto.vl_total = vl_total

    #         result:CompraProdutoModel = self.compra_produto_repository.create(nova_compra_produto)
    #         if result is None:
    #             self.listErrors.append("Erro ao cadastrar compra x produto") # 500
    #             return result
        
    #     return result_compra
    
    # def update(self, id, json):
    #     c, cp, p = self.compra_repository.find(id)
    #     compra_encontrado: CompraModel = c

    #     if compra_encontrado is None:
    #         self.listErrors.append("Compra não encontrada!") # 404
    #         return False

    #     fornecedor = json.get('fornecedor')
    #     dt_compra = json.get('dt_compra')
    #     compra_produto = json.get('compra_produto')

    #     if not fornecedor or not dt_compra or not compra_produto:
    #         self.listErrors.append("Dados incompletos!") # 400
    #         return False

    #     for item in compra_produto:
    #         quantidade = item['quantidade']
    #         if not quantidade:
    #             self.listErrors.append("O campo 'quantidade' do compra_produto é obrigatório.") # 400
    #             return False

    #     compra_encontrado.fornecedor = fornecedor
    #     compra_encontrado.dt_compra = dt_compra

    #     result = self.compra_repository.update(id, compra_encontrado)
    #     if result == True:
    #         compra_produto_encontrado = self.compra_produto_repository.findByCompraId(id)

    #         itens_para_remover = [item for item in compra_produto_encontrado if item not in compra_produto]
    #         for item in itens_para_remover:
    #             if self.compra_produto_repository.destroy(item.id) == False:
    #                 self.listErrors.append("Não foi possivel deletar Compra x Produto") # 500
    #                 return False
                
    #         for item in compra_produto:
    #             id_produto = item['produto']['id_produto']
    #             quantidade = item['quantidade']
    #             vl_unidade = item['vl_unidade']
    #             vl_total = item['vl_total']

    #             if vl_total is not None and vl_unidade is None:
    #                 vl_unidade = vl_total / quantidade

    #             if vl_unidade is not None and vl_total is None:
    #                 vl_total = vl_unidade * quantidade

    #             nova_compra_produto = CompraProdutoModel()
    #             nova_compra_produto.id_compra = id
    #             nova_compra_produto.id_produto = id_produto
    #             nova_compra_produto.quantidade = quantidade
    #             nova_compra_produto.vl_unidade = vl_unidade
    #             nova_compra_produto.vl_total = vl_total

    #             result_cp:CompraProdutoModel = self.compra_produto_repository.create(nova_compra_produto)
    #             if result_cp is None:
    #                 self.listErrors.append("Erro ao cadastrar Compra x Produto") # 404
    #                 return False
                
    #     return result

    # def destroy(self, id):
    #     lista_compra_produto = self.compra_produto_repository.findByCompraId(id)
    #     if lista_compra_produto is not None:
    #         result_compraProduto = self.compra_produto_repository.destroyByCompraId(id)
    #         if result_compraProduto == True:
    #             result = self.compra_repository.destroy(id)
    #             if result == False:
    #                 self.listErrors.append("Error ao deletar a Compra") # 500
    #                 return False
    #             return result
    #         else:
    #             self.listErrors.append("Error ao deletar em Compra X Produto") # 500
    #             return False
    #     else:
    #         result = self.compra_repository.destroy(id)
    #         if result == False:
    #             self.listErrors.append("Error ao deletar a Compra") # 500
    #             return False
    #         return result

    # def searchCompraProductId(self, id):
    #     compras = self.compra_repository.searchCompraProductId(id)
    #     serializados = []

    #     if len(compras) > 0:
    #         for c, cp, p in compras:
    #             serializados.append(c.to_dict())

    #     return serializados
    
    def get_all_errors(self):
        return self.listErrors
