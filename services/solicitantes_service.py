from models.solicitante_model import SolicitantesModel


class SolicitantesService:
    def __init__(self):
        self.solicitantes_model = SolicitantesModel()

    def cadastrar_solicitante(self, nome: str, regional: int) -> None:
        self.solicitantes_model.create_solicitante(nome, regional)

    def listar_solicitantes(self) -> list:
        return self.solicitantes_model.get_solicitantes()