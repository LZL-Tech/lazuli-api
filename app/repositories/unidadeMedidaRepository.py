from models.unidadeMedidaModel import UnidadeMedidaModel
from repositories.baseRepository import BaseRepository


class UnidadeMedidaRepository(BaseRepository):
    def __init__(self):
        super().__init__(UnidadeMedidaModel)