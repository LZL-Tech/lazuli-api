from typing import List
from models.unidadeMedidaModel import UnidadeMedidaModel
from repositories.unidadeMedidaRepository import UnidadeMedidaRepository

class UnidadeMedidaService:
    def __init__(self):
        self.unidade_medida_repository = UnidadeMedidaRepository()
        self.listErrors = []

    def findAll(self):
        unidades_medida: List[UnidadeMedidaModel] = self.unidade_medida_repository.findAll()
        serializados = []

        for unidade_medida in unidades_medida:
            serializados.append(unidade_medida.to_dict())
       
        return serializados

    def get_all_errors(self):
        return self.listErrors