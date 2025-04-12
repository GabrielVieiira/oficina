from models.combustiveis_model import CombustiveisModel

class CombustiveisService:
    def __init__(self):
        self.combustivel_model = CombustiveisModel()

    def listar_combustiveis(self) -> list:
        try:
            combustiveis = self.combustivel_model.get_combustiveis()
            if combustiveis:
                return combustiveis
            else:
                return []
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de combustíveis: {e}')