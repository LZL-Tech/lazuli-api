import datetime
from app import app
from flask import Response, abort, jsonify, request, url_for
from itertools import groupby

from services.vendaService import VendaService



vendaService = VendaService()


@app.route('/venda/<int:id>', methods=['GET'])
def get_venda(id):
    venda = vendaService.find(id)
    if venda is not None:
        response = jsonify(venda)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
       abort(404, 'Recurso não encontrado')

@app.route('/venda', methods=['GET'])
def get_vendas():
    vendas = vendaService.findAll()
    response = jsonify(vendas)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# @app.route('/venda', methods=['POST'])
# def add_venda():
#     nm_cliente: str = request.json.get('nm_cliente')
#     dt_venda: datetime = request.json.get('dt_venda')
#     venda_produto = request.json.get('venda_produto')

#     nova_venda = VendaModel()
#     nova_venda.nm_cliente = nm_cliente
#     nova_venda.dt_venda = dt_venda

#     result_venda: VendaModel = venda_repository.create(nova_venda)

#     if result_venda is None:
#         abort(400, 'Error ao cadastrar venda')

#     for item in venda_produto:
#         id_produto = item['id_produto']
#         quantidade = item['quantidade']
#         preco_unidade = item['preco_unidade']

#         nova_venda_produto = VendaProdutoModel()
#         nova_venda_produto.id_venda = result_venda.id
#         nova_venda_produto.id_produto = id_produto
#         nova_venda_produto.quantidade = quantidade
#         nova_venda_produto.preco_unidade = preco_unidade

#         result: VendaProdutoModel = venda_produto_repository.create(nova_venda_produto)

#         #Validando se deu certo a operação
#         if result is None:
#             abort(400, 'Error ao cadastrar venda x produto')

#     response = jsonify(None)
#     response.status_code = 201
#     response.headers['Location'] = url_for('get_venda', id=result_venda.id)
#     return response

# @app.route('/venda/<int:id>', methods=['PUT'])
# def update_venda(id):
#     venda_encontrado: VendaModel = venda_repository.find(id)

#     if venda_encontrado is None:
#          abort(404, message="'Not Found")

#     nm_cliente: str = request.json.get('nm_cliente')
#     dt_venda: datetime = request.json.get('dt_venda')
#     venda_produto: VendaProdutoModel = request.json.get('venda_produto')

#     venda_encontrado.nm_cliente = nm_cliente
#     venda_encontrado.dt_venda = dt_venda

#     result = venda_repository.update(id, venda_encontrado)

#     venda_produto_encontrado = venda_produto_repository.findByVendaId(id)

#     if result == True:

#         itens_para_remover = [item for item in venda_produto_encontrado if item not in venda_produto]
#         for item in itens_para_remover:
#            venda_produto_repository.destroy(item.id)

#         for item in venda_produto:
#             vpe_item = next((item2 for item2 in venda_produto_encontrado if item['id_produto'] == item2.id_produto
#             and item['quantidade'] == item2.quantidade and item['preco_unidade'] == item2.preco_unidade), None)
#             if vpe_item:
#                 vpe_item.id_produto = item['id_produto']
#                 vpe_item.quantidade =  item['quantidade']
#                 vpe_item.preco_unidade = item['preco_unidade']

#                 result = venda_produto_repository.update(vpe_item.id, vpe_item)
#             else:
#                 nova_venda_produto = VendaProdutoModel()
#                 nova_venda_produto.id_venda = id
#                 nova_venda_produto.id_produto = item['id_produto']
#                 nova_venda_produto.quantidade = item['quantidade']
#                 nova_venda_produto.preco_unidade = item['preco_unidade']

#                 result_venda_produto: VendaProdutoModel = venda_produto_repository.create(nova_venda_produto)

#         return Response(status=204)
#     else:
#         abort(400, 'Error ao atualizar venda x produto')
    
# @app.route('/venda/<int:id>', methods=['DELETE'])
# def delete_venda(id):
#     result_find = venda_produto_repository.findByVendaId(id)
#     if result_find is None:
#         abort(404, 'Venda não encontrada!')

#     result_vendaProduto = venda_produto_repository.destroyByVendaId(id)
#     if result_vendaProduto == True:
#         result = venda_repository.destroy(id)
#         if result == True:
#             return Response(status=204)
#         else:
#             abort(400, 'Error')
#     else:
#          abort(400, 'Error')

# @app.route('/venda/produto/<int:id>', methods=['GET'])
# def searchVendaProductId(id):
#     vendas = venda_repository.searchVendaProductId(id)
#     serializados = []

#     if len(vendas) > 0:
#         for key, group in groupby(vendas, lambda x: x[0]):
#             venda_serializado = {
#                 'id_venda': key.id,
#                 'nm_cliente': key.nm_cliente,
#                 'dt_venda': key.dt_venda.strftime('%Y-%m-%d'),
#                 "venda_produto": []
#             }
#             for item in group: #venda.vendaProdutos:
#                 venda_serializado["venda_produto"].append({
#                     "id_venda_produto": item[1].id,
#                     "id_produto": item[1].id_produto,
#                     "id_venda": item[1].id_venda,
#                     "preco_unidade": float(item[1].preco_unidade),
#                     "quantidade": item[1].quantidade,
#                     "produto": {
#                         'id_produto': item[2].id,
#                         'descricao': item[2].descricao,
#                         'marca': item[2].marca,
#                         'qtd_estoque': item[2].qtd_estoque,
#                         'preco': item[2].preco,
#                         'id_unidade_medida': item[2].id_unidade_medida,
#                         'id_tipo_produto': item[2].id_tipo_produto,
#                         'tipo_produto': {
#                             'id_tipo_produto': item[2].tipo_produto.id,
#                             'descricao': item[2].tipo_produto.descricao
#                         },
#                         'unidade_medida': {
#                             'id_unidade_medida':item[2].unidade_medida.id,
#                             'descricao': item[2].unidade_medida.descricao,
#                             'simbolo': item[2].unidade_medida.simbolo
#                         }
#                     }
#                 })
#             serializados.append(venda_serializado)

#     response = jsonify(serializados)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response