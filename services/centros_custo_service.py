from models.centros_custo_model import CentroCustoModel


class CentroCustoService:
    def __init__(self):
        self.centro_custo_model = CentroCustoModel()

    def listar_centros_custo(self) -> list:
        return self.centro_custo_model.get_centros_custo()

    # def cadastrar_centro_custo(self, nome: str) -> None:
    #     try:
    #         self.centro_custo_model.create_centro_custo(nome)
    #     except Exception as e:
    #         raise Exception(f"Erro ao cadastrar centro de custo: {e}")