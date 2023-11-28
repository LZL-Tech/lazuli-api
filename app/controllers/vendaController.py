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

@app.route('/venda', methods=['POST'])
def add_venda():
    venda = vendaService.create(request.json)
    if venda is not None:
        response = jsonify(venda.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('get_venda', id=venda.id)
        return response
    else:
        abort(400, 'Error')

@app.route('/venda/<int:id>', methods=['PUT'])
def update_venda(id):
    result = vendaService.update(id, request.json)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')
    
@app.route('/venda/<int:id>', methods=['DELETE'])
def delete_venda(id):
    result = vendaService.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        erro = vendaService.get_all_errors()
        return jsonify({"message": erro[0]}), 409

@app.route('/venda/produto/<int:id>', methods=['GET'])
def searchVendaProductId(id):
    venda = vendaService.searchVendaProductId(id)
    if venda is not None:
        response = jsonify(venda)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
       abort(404, 'Recurso não encontrado')