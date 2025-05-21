from models.prioridades_model import PrioridadesModel

class PrioridadesService:
    def __init__(self):
        self.prioridades_model = PrioridadesModel()

    def listar_prioridades(self) -> list[dict]:
        prioridades = self.prioridades_model.get_prioridades()
        return prioridades or []