from app import app
from flask import Response, abort, jsonify, request, url_for

from services.compraService import CompraService

compraService = CompraService()


@app.route('/compra/<int:id>', methods=['GET'])
def get_compra(id):
    compra = compraService.find(id)
    if compra is not None:
        response = jsonify(compra)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
       abort(404, 'Recurso não encontrado')

@app.route('/compra', methods=['GET'])
def get_compras():
    produtos = compraService.findAll()
    response = jsonify(produtos)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/compra', methods=['POST'])
def add_compra():
    compra = compraService.create(request.json)
    if compra is not None:
        response = jsonify(compra.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('get_compra', id=compra.id)
        return response
    else:
        abort(400, 'Error')

@app.route('/compra/<int:id>', methods=['PUT'])
def update_compra(id):
    result = compraService.update(id, request.json)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/compra/<int:id>', methods=['DELETE'])
def delete_compra(id):
    result = compraService.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        erro = compraService.get_all_errors()
        return jsonify({"message": erro[0]}), 409

@app.route('/compra/produto/<int:id>', methods=['GET'])
def searchCompraProductId(id):
    compra = compraService.searchCompraProductId(id)
    if compra is not None:
        response = jsonify(compra)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
       abort(404, 'Recurso não encontrado')