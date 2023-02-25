from flask import request, abort, jsonify, Response
from app import app
from domain.models import Produto
from repository.repositories import ProdutoRepository

produtoRepository = ProdutoRepository()

@app.route('/')
@app.route('/home')
def index():
    return "Hello, World!"

@app.route('/produto/<int:id>', methods=['GET'])
def get_product(id):
    produtoEncontrado = produtoRepository.find(id)
    if produtoEncontrado is not None:
        produto = {
            'id': produtoEncontrado.id,
            'descricao': produtoEncontrado.descricao,
            'quantidade':produtoEncontrado.quantidade
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