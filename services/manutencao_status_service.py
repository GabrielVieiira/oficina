from models.manutencao_status_model import ManutencaoStatusModel

class ManutencaoStatusService:
    def __init__(self):
        self.model = ManutencaoStatusModel()

    def listar_manutencao_status(self) -> list:
        return self.model.get_manutencao_status()