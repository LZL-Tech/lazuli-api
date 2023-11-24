from app import app
from flask import jsonify
from services.tipoProdutoService import TipoProdutoService

tipoProdutoService = TipoProdutoService()

@app.route('/tipo_produto', methods=['GET'])
def get_tipo_produtos():
    tipoProdutos = tipoProdutoService.findAll()
    response = jsonify(tipoProdutos)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
