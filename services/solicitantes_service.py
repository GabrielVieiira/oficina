from models.solicitante_model import SolicitantesModel


class SolicitantesService:
    def __init__(self):
        self.solicitantes_model = SolicitantesModel()

    def cadastrar_solicitante(self, nome: str, cargo: str, regional: str) -> None:
        self.solicitantes_model.cadastrar_solicitante(nome, cargo, regional)

    def listar_solicitantes(self) -> list:
        return self.solicitantes_model.listar_solicitantes()