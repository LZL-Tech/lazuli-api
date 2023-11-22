from app import app
from flask import Response, abort, jsonify, request, url_for
from itertools import groupby

from models.compraModel import CompraModel
from models.compraProdutoModel import CompraProdutoModel
from repositories.compraRepository import CompraRepository
from repositories.compraProdutoRepository import CompraProdutoRepository

compra_repository = CompraRepository()
compra_produto_repository = CompraProdutoRepository()

@app.route('/compra/<int:id>', methods=['GET'])
def get_compra(id):
    compraEncontrado: CompraModel = compra_repository.find(id)
    result = []
    for key, group in groupby(compraEncontrado, lambda x: x[0]):
        compra = {
            "id_compra": key.id,
            "fornecedor": key.fornecedor,
            "dt_compra": key.dt_compra.strftime('%Y-%m-%d'),
            "produto": []
        }
        for item in group:
            compra["produto"].append({
                "id_produto": item[2].id,
                "descricao": item[2].descricao,
                "quantidade": float(item[1].quantidade),
                "vl_unidade": float(item[1].vl_unidade),
                "vl_total": float(item[1].vl_total)
            })
        result.append(compra)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/compra', methods=['GET'])
def get_compras():
    compras = compra_repository.findAll()
    result = []
    for key, group in groupby(compras, lambda x: x[0]):
        compra = {
            "id_compra": key.id,
            "fornecedor": key.fornecedor,
            "dt_compra": key.dt_compra.strftime('%Y-%m-%d'),
            "produto": []
        }
        for item in group:
            compra["produto"].append({
                "id_produto": item[2].id,
                "descricao": item[2].descricao,
                "quantidade": float(item[1].quantidade),
                "vl_unidade": float(item[1].vl_unidade),
                "vl_total": float(item[1].vl_total)
            })
        result.append(compra)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/compra', methods=['POST'])
def add_compra():
    fornecedor = request.json.get('fornecedor')
    dt_compra = request.json.get('dt_compra')
    compra_produto = request.json.get('compra_produto')

    if not fornecedor or not dt_compra or not compra_produto:
        abort(400, message="'Dados incompletos.")

    nova_compra = CompraModel()
    nova_compra.fornecedor = fornecedor
    nova_compra.dt_compra = dt_compra

    result_compra: CompraModel = compra_repository.create(nova_compra)

    if result_compra is None:
        abort(400, 'Error ao cadastrar compra')

    for item in compra_produto:
        id_produto = item['produto']['id_produto']
        descricao = item['produto']['descricao']

        quantidade = item['quantidade']
        vl_unidade = item['vl_unidade']
        vl_total = item['vl_total']

        if not quantidade:
            abort(400, message="O campo 'quantidade' é obrigatório.")

        if vl_total is not None and vl_unidade is None:
            vl_unidade = vl_total / quantidade

        if vl_unidade is not None and vl_total is None:
            vl_total = vl_unidade * quantidade

        nova_compra_produto = CompraProdutoModel()
        nova_compra_produto.id_compra = result_compra.id
        nova_compra_produto.id_produto = id_produto
        nova_compra_produto.quantidade = quantidade
        nova_compra_produto.vl_unidade = vl_unidade
        nova_compra_produto.vl_total = vl_total

        result:CompraProdutoModel = compra_produto_repository.create(nova_compra_produto)

        #Validando se deu certo a operação
        if result is None:
            abort(400, 'Error ao cadastrar compra x produto')

    response = jsonify(None)
    response.status_code = 201
    response.headers['Location'] = url_for('get_compra', id=result_compra.id)
    return response

@app.route('/compra/<int:id>', methods=['PUT'])
def update_compra(id):
    data = compra_repository.find(id)
    compra_encontrado: CompraModel = data.Compra

    if compra_encontrado is None:
         abort(404, message="'Not Found")

    fornecedor = request.json.get('fornecedor')
    dt_compra = request.json.get('dt_compra')
    compra_produto = request.json.get('compra_produto')

    if not fornecedor or not dt_compra or not compra_produto:
            abort(400, message="'Dados incompletos!")

    for item in compra_produto:
        quantidade = item['quantidade']
        if not quantidade:
            abort(400, message="O campo 'quantidade' do compra_produto é obrigatório.")

    compra_encontrado.fornecedor = fornecedor
    compra_encontrado.dt_compra = dt_compra

    result = compra_repository.update(id, compra_encontrado)

    compra_produto_encontrado = compra_produto_repository.findByCompraId(id)

    if result == True:

        itens_para_remover = [item for item in compra_produto_encontrado if item not in compra_produto]
        for item in itens_para_remover:
           compra_produto_repository.destroy(item.id)

        for item in compra_produto:
            id_produto = item['produto']['id_produto']
            quantidade = item['quantidade']
            vl_unidade = item['vl_unidade']
            vl_total = item['vl_total']

            if vl_total is not None and vl_unidade is None:
                vl_unidade = vl_total / quantidade

            if vl_unidade is not None and vl_total is None:
                vl_total = vl_unidade * quantidade

            nova_compra_produto = CompraProdutoModel()
            nova_compra_produto.id_compra = id
            nova_compra_produto.id_produto = id_produto
            nova_compra_produto.quantidade = quantidade
            nova_compra_produto.vl_unidade = vl_unidade
            nova_compra_produto.vl_total = vl_total

            result:CompraProdutoModel = compra_produto_repository.create(nova_compra_produto)

            if result is None:
                abort(400, 'Error ao cadastrar compra x produto')
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/compra/<int:id>', methods=['DELETE'])
def delete_compra(id):
    result_find = compra_produto_repository.findByCompraId(id)
    if result_find is None:
        abort(404, 'Compra não encontrada!')

    result_compraProduto = compra_produto_repository.destroyByCompraId(id)
    if result_compraProduto == True:
        result = compra_repository.destroy(id)
        if result == True:
            return Response(status=204)
        else:
            abort(400, 'Error')
    else:
         abort(400, 'Error')

@app.route('/compra/produto/<int:id>', methods=['GET'])
def searchCompraProductId(id):
    compras = compra_repository.searchCompraProductId(id)
    result = []
    for key, group in groupby(compras, lambda x: x[0]):
        compra = {
            "id_compra": key.id,
            "fornecedor": key.fornecedor,
            "dt_compra": key.dt_compra.strftime('%Y-%m-%d'),
            "produto": []
        }
        for item in group:
            compra["produto"].append({
                "id_produto": item[2].id,
                "descricao": item[2].descricao,
                "quantidade": float(item[1].quantidade),
                "vl_unidade": float(item[1].vl_unidade),
                "vl_total": float(item[1].vl_total)
            })
        result.append(compra)

    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response