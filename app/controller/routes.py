from flask import request, abort, jsonify, Response
from app import app
from domain.produto import Produto
from repository.repositories import ProdutoRepository

produtoRepository = ProdutoRepository()

@app.route('/')
@app.route('/home')
def index():
    return "Hello, World!"

@app.route('/produto/<int:id>', methods=['GET'])
def get_product(id):
    produto_encontrado = produtoRepository.find(id)
    if produto_encontrado is not None:
        produto = {
            'id': produto_encontrado.id,
            'descricao': produto_encontrado.descricao,
            'quantidade':produto_encontrado.quantidade
        }
        return jsonify(produto)
    else:
       abort(400, 'Error')


@app.route('/produto', methods=['GET'])
def get_products():  
    produtos = produtoRepository.findAll()
    lista_produtos = [{'id': produto.id, 'descricao': produto.descricao, 'quantidade': produto.quantidade} for produto in produtos]
    return jsonify(lista_produtos)

@app.route('/produto', methods=['POST'])
def add_product():
    descricao = request.json['descricao']
    quantidade = request.json['quantidade']
    novo_produto = Produto(descricao, quantidade)
    result = produtoRepository.create(novo_produto)
    if result == True:
        return Response(status=201)
    else:
        abort(400, 'Error')


@app.route('/produto/<int:id>', methods=['PUT'])
def update_product(id):
    produtoEncontrado = produtoRepository.find(id)

    descricao = request.json['descricao']
    quantidade = request.json['quantidade']

    produtoEncontrado.descricao = descricao
    produtoEncontrado.quantidade = quantidade

    result = produtoRepository.update(id, produtoEncontrado)

    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/produto/<int:id>', methods=['DELETE'])
def delete_product(id):
    result = produtoRepository.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

        
@app.route('/compra/<int:id>', methods=['GET'])
def get_compra(id):
    compraEncontrada = compraRepository.find(id)
    if compraEncontrada is not None:
        compra = {
            'id_compra': compraEncontrada.id,
            'fornecedor': compraEncontrada.fornecedor,
            'dt_compra':compraEncontrada.dt_compra
        }

        return jsonify(compra)
    else:
       abort(400, 'Error')

@app.route('/compra_produto/<int:id>', methods=['GET'])
def get_compra_produto(id):
    compraProdutoEncontrada = compraProdutoRepository.find(id)
    if compraProdutoEncontrada is not None:
        compraProduto = {
            'id_compra_produto': compraProdutoEncontrada.id_compra_produto,
            'id_compra': compraProdutoEncontrada.id_compra,
            'id_produto': compraProdutoEncontrada.id_produto,
            'quantidade': compraProdutoEncontrada.quantidade,
            'vl_unidade': compraProdutoEncontrada.vl_unidade,
            'vl_total': compraProdutoEncontrada.vl_total
        }

        return jsonify(compraProduto)
    else: 
        abort(400, 'Error')