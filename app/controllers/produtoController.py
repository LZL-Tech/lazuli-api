from app import app
from flask import Response, abort, jsonify, request, url_for

from services.produtoService import ProdutoService

produtoService = ProdutoService()

@app.route('/produto/<int:id>', methods=['GET'])
def get_product(id):
    produto = produtoService.find(id)
    if produto is not None:
        return jsonify(produto)
    else:
       abort(404, 'Recurso não encontrado')

@app.route('/produto', methods=['GET'])
def get_products():
    produtos = produtoService.findAll()
    return jsonify(produtos)

@app.route('/produto', methods=['POST'])
def add_product():
    produto = produtoService.create(request.json)
    if produto is not None:
        response = jsonify(produto.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('get_product', id=produto.id)
        return response
    else:
        abort(400, 'Error')

@app.route('/produto/<int:id>', methods=['PUT'])
def update_product(id):
    result = produtoService.update(id, request.json)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/produto/<int:id>', methods=['DELETE'])
def delete_product(id):
    result = produtoService.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        erro = produtoService.get_all_errors()
        return jsonify({"message": erro[0]}), 409


@app.route('/produto/filter', methods=['GET'])
def get_filter_produtos():
    produtos = produtoService.findAllSearch(request.args)
    response = jsonify(produtos)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response