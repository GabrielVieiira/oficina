from models.mecanicos_model import MecanicosModel

class MecanicosService:
    def __init__(self):
        self.mecanico_model = MecanicosModel()

    def listar_mecanicos(self) -> list:
        return self.mecanico_model.get_mecanico()

    def buscar_funcionario(self, id: int) -> dict:
        return self.mecanico_model.get_mecanico_by_id(id)
    
    def cadastrar_funcionario(self, nome: str, cargo_id: int, regional_id: int) -> None:
        try:
            self.mecanico_model.create_mecanico(nome, cargo_id, regional_id)
        except Exception as e:
            raise Exception(f"Erro ao cadastrar funcionário: {e}")

    def listar_cargos(self) -> list:
        return self.mecanico_model.get_cargos()