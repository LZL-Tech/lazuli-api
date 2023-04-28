from typing import List
from domain.models import Produto, UnidadeMedida, TipoProduto
from flask import Response, abort, jsonify, request
from flask_cors import cross_origin
from repository.repositories import *
from itertools import groupby

from app import app

produto_repository = ProdutoRepository()
tipo_produto_repository = TipoProdutoRepository()
unidade_medida_repository = UnidadeMedidaRepository()
compra_repository = CompraRepository()

@app.route('/')
@app.route('/home')
def index():
    return "Hello, World!"

@app.route('/produto/<int:id>', methods=['GET'])
def get_product(id):
    produtoEncontrado = produto_repository.find(id)
    if produtoEncontrado is not None:
        produto = {
            'id_produto': produtoEncontrado.id,
            'descricao': produtoEncontrado.descricao,
            'marca':produtoEncontrado.marca,
            'qtd_estoque':produtoEncontrado.qtd_estoque,
            'preco':produtoEncontrado.preco,
            'id_unidade_medida':produtoEncontrado.id_unidade_medida,
            'id_tipo_produto':produtoEncontrado.id_tipo_produto
        }

        return jsonify(produto)
    else:
       abort(400, 'Error')

@app.route('/produto', methods=['GET'])
def get_products():
    produtos = produto_repository.findAll()
    serializados = []

    if len(produtos) > 0:
        for produto in produtos:
            produto_serializado = {
                'id_produto': produto.id,
                'descricao': produto.descricao,
                'marca':produto.marca,
                'qtd_estoque':produto.qtd_estoque,
                'preco':produto.preco,
                'id_unidade_medida':produto.id_unidade_medida,
                'id_tipo_produto':produto.id_tipo_produto,
                'tipo_produto': {
                    'id_tipo_produto': produto.tipo_produto.id,
                    'descricao': produto.tipo_produto.descricao
                },
                'unidade_medida': {
                    'id_unidade_medida': produto.unidade_medida.id,
                    'descricao': produto.unidade_medida.descricao,
                    'simbolo': produto.unidade_medida.simbolo
                }
            }

            serializados.append(produto_serializado)

    return jsonify(serializados)

@app.route('/produto', methods=['POST'])
def add_product():
    #Entrada de dados request.json.get('descricao')
    descricao = request.json.get('descricao')
    marca = request.json.get('marca')
    qtd_estoque = request.json.get('qtd_estoque')
    preco = request.json.get('preco')
    unidade_medida = request.json.get('unidade_medida')
    tipo_produto = request.json.get('tipo_produto')

    novo_produto = Produto()

    #Criando objeto
    tipoProdutoEncontrado: Produto = tipo_produto_repository.find(tipo_produto['id_tipo_produto'])
    if tipoProdutoEncontrado is not None:
        if tipoProdutoEncontrado.descricao.upper() == 'INGREDIENTE':
            novo_produto.descricao = descricao
            novo_produto.qtd_estoque = qtd_estoque
            novo_produto.id_unidade_medida = unidade_medida['id_unidade_medida']
            novo_produto.id_tipo_produto = tipo_produto['id_tipo_produto']
            novo_produto.marca = marca
        else:
            novo_produto.descricao = descricao
            novo_produto.qtd_estoque = qtd_estoque
            novo_produto.id_unidade_medida = unidade_medida['id_unidade_medida']
            novo_produto.id_tipo_produto = tipo_produto['id_tipo_produto']
            novo_produto.preco = preco

    #Inserindo dado no banco de dados
    result = produto_repository.create(novo_produto)

    #Validando se deu certo a operação
    if result == True:
        return Response(status=201)
    else:
        abort(400, 'Error')

@app.route('/produto/<int:id>', methods=['PUT'])
def update_product(id):
    produto_encontrado: Produto = produto_repository.find(id)

    descricao = request.json.get('descricao')
    marca = request.json.get('marca')
    qtd_estoque = request.json.get('qtd_estoque')
    preco = request.json.get('preco')
    id_unidade_medida = request.json.get('id_unidade_medida')
    id_tipo_produto = request.json.get('id_tipo_produto')

    produto_encontrado.descricao = descricao
    produto_encontrado.qtd_estoque = qtd_estoque
    produto_encontrado.id_unidade_medida = id_unidade_medida
    produto_encontrado.id_tipo_produto = id_tipo_produto
    produto_encontrado.marca = marca
    produto_encontrado.preco = preco

    result = produto_repository.update(id, produto_encontrado)

    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/produto/<int:id>', methods=['DELETE'])
def delete_product(id):
    result = produto_repository.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/produto/filter', methods=['GET'])
def get_filter_produtos():
    id_tipo = request.args.get('id_tipo')
    descricao = request.args.get('descricao')
    serializados = []

    produtos = produto_repository.findAllSearch(id_tipo, descricao)
    if len(produtos) > 0:
        for produto in produtos:
            produto_serializado = {
                'id_produto': produto.id,
                'descricao': produto.descricao,
                'marca':produto.marca,
                'qtd_estoque':produto.qtd_estoque,
                'preco':produto.preco,
                'id_unidade_medida':produto.id_unidade_medida,
                'id_tipo_produto':produto.id_tipo_produto,
                'tipo_produto': {
                    'id_tipo_produto': produto.tipo_produto.id,
                    'descricao': produto.tipo_produto.descricao
                },
                'unidade_medida': {
                    'id_unidade_medida': produto.unidade_medida.id,
                    'descricao': produto.unidade_medida.descricao,
                    'simbolo': produto.unidade_medida.simbolo
                }
            }

    response = jsonify(serializados)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/tipo_produto', methods=['GET'])
def get_tipo_produtos():
    tipo_produtos = tipo_produto_repository.findAll()
    serializados = []

    if len(tipo_produtos) > 0:
        for tipo_produto in tipo_produtos:
            tipo_produto_serializado = {
                'id_tipo_produto': tipo_produto.id,
                'descricao': tipo_produto.descricao
            }
            serializados.append(tipo_produto_serializado)

    response = jsonify(serializados)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/unidade_medida', methods=['GET'])
def get_unidades_medidas():
    unidades_medida: List[UnidadeMedida] = unidade_medida_repository.findAll()
    response = []
    for unidade_medida in unidades_medida:
        response.append({
            'id_unidade_medida': unidade_medida.id,
            'descricao': unidade_medida.descricao,
            'simbolo': unidade_medida.simbolo
        })
    return jsonify(response)

@app.route('/compra', methods=['GET'])
def get_compras():
    compras = compra_repository.findAll()
    result = []
    for key, group in groupby(compras, lambda x: x[0]):
        compra = {
            "id_compra": key.id,
            "fornecedor": key.fornecedor,
            "dt_compra": key.dt_compra.strftime('%d/%m/%Y'),
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
