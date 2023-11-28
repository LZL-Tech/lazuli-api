import datetime
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

    def create(self, json):
        nm_cliente: str = json.get('nm_cliente')
        dt_venda: datetime = json.get('dt_venda')
        venda_produto = json.get('venda_produto')

        nova_venda = VendaModel()
        nova_venda.nm_cliente = nm_cliente
        nova_venda.dt_venda = dt_venda

        result_venda: VendaModel = self.venda_repository.create(nova_venda)
        if result_venda is None:
            self.listErrors.append("Erro ao cadastrar venda") # 400
            return result_venda

        for item in venda_produto:
            id_produto = item['id_produto']
            quantidade = item['quantidade']
            preco_unidade = item['preco_unidade']

            nova_venda_produto = VendaProdutoModel()
            nova_venda_produto.id_venda = result_venda.id
            nova_venda_produto.id_produto = id_produto
            nova_venda_produto.quantidade = quantidade
            nova_venda_produto.preco_unidade = preco_unidade

            result: VendaProdutoModel = self.venda_produto_repository.create(nova_venda_produto)
            if result is None:
                self.listErrors.append("Error ao cadastrar venda x produto") # 400
                return result
            
        return result_venda
    
    def update(self, id, json):
        v, vp, p = self.venda_repository.find(id)
        venda_encontrado: VendaModel = v

        if venda_encontrado is None:
            self.listErrors.append("Venda não encontrada") # 404
            return result

        nm_cliente: str = json.get('nm_cliente')
        dt_venda: datetime = json.get('dt_venda')

        venda_produto: VendaProdutoModel = json.get('venda_produto')
        venda_encontrado.nm_cliente = nm_cliente
        venda_encontrado.dt_venda = dt_venda

        result = self.venda_repository.update(id, venda_encontrado)
        if result == True:
            venda_produto_encontrado = self.venda_produto_repository.findByVendaId(id)

            itens_para_remover = [item for item in venda_produto_encontrado if item not in venda_produto]
            for item in itens_para_remover:
                if self.venda_produto_repository.destroy(item.id) == False:
                    self.listErrors.append("Não foi possivel deletar Venda x Produto") # 500
                    return False

            for item in venda_produto:
                vpe_item = next((item2 for item2 in venda_produto_encontrado if item['id_produto'] == item2.id_produto
                and item['quantidade'] == item2.quantidade and item['preco_unidade'] == item2.preco_unidade), None)
                if vpe_item:
                    vpe_item.id_produto = item['id_produto']
                    vpe_item.quantidade =  item['quantidade']
                    vpe_item.preco_unidade = item['preco_unidade']

                    if self.venda_produto_repository.update(vpe_item.id, vpe_item) == False:
                        self.listErrors.append("Não foi possivel atualizar Venda x Produto") # 500
                        return False
                else:
                    nova_venda_produto = VendaProdutoModel()
                    nova_venda_produto.id_venda = id
                    nova_venda_produto.id_produto = item['id_produto']
                    nova_venda_produto.quantidade = item['quantidade']
                    nova_venda_produto.preco_unidade = item['preco_unidade']

                    if self.venda_produto_repository.create(nova_venda_produto) == False:
                        self.listErrors.append("Não foi possivel criar Venda x Produto") # 500
                        return False
                    
            return True
        else:
            self.listErrors.append("Error ao atualizar venda x produto") # 400
            return False

    def destroy(self, id):
        lista_venda_produto = self.venda_produto_repository.findByVendaId(id)
        if lista_venda_produto is not None:
            result_vendaProduto = self.venda_produto_repository.destroyByVendaId(id)
            if result_vendaProduto == True:
                result = self.venda_repository.destroy(id)
                if result == False:
                    self.listErrors.append("Error ao deletar a Venda") # 500
                    return False
                return result
            else:
                self.listErrors.append("Error ao deletar a Venda x Produto") # 500
                return False
        else:
            result = self.venda_repository.destroy(id)
            if result == False:
                self.listErrors.append("Error ao deletar a Venda") # 500
                return False
            return result
       
    def searchVendaProductId(self, id):
        vendas = self.venda_repository.searchVendaProductId(id)
        serializados = []

        if len(vendas) > 0:
            for v, vp, p in vendas:
                serializados.append(v.to_dict())

        return serializados
    
    def get_all_errors(self):
        return self.listErrors
