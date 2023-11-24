from app import app
from flask import jsonify
from services.unidadeMedidaService import UnidadeMedidaService

unidadeMedidaService = UnidadeMedidaService()

@app.route('/unidade_medida', methods=['GET'])
def get_unidades_medidas():
    unidadeMedidas = unidadeMedidaService.findAll()
    response = jsonify(unidadeMedidas)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response