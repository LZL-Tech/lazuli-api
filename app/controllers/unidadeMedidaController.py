from app import app
from flask import jsonify
from typing import List

from models.unidadeMedidaModel import UnidadeMedidaModel
from repositories.unidadeMedidaRepository import UnidadeMedidaRepository


unidade_medida_repository = UnidadeMedidaRepository()

@app.route('/unidade_medida', methods=['GET'])
def get_unidades_medidas():
    unidades_medida: List[UnidadeMedidaModel] = unidade_medida_repository.findAll()
    serializados = []

    for unidade_medida in unidades_medida:
        serializados.append({
            'id_unidade_medida': unidade_medida.id,
            'descricao': unidade_medida.descricao,
            'simbolo': unidade_medida.simbolo
        })

    response = jsonify(serializados)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response