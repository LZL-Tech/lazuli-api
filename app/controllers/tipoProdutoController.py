from app import app
from flask import jsonify
from typing import List

from models.tipoProdutoModel import TipoProdutoModel
from repositories.tipoProdutoRepository import TipoProdutoRepository


tipo_produto_repository = TipoProdutoRepository()

@app.route('/tipo_produto', methods=['GET'])
def get_tipo_produtos():
    tipo_produtos: List[TipoProdutoModel] = tipo_produto_repository.findAll()
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
