from models.manutencoes_model import ManutencoesModel

class ManutencoesService:
    def __init__(self):
        self.manutencoes_model = ManutencoesModel()

    def registrar_entrada(self, patrimonio_id: int, mecanico_id: int, problema: str) -> None:
        self.manutencoes_model.registrar_entrada(patrimonio_id, mecanico_id, problema)

    def iniciar_manutencao(self, manutencao_id: int) -> None:
        self.manutencoes_model.iniciar_manutencao(manutencao_id)

    def concluir_manutencao(self, manutencao_id: int, solucao: str, custo: float) -> None:
        self.manutencoes_model.concluir_manutencao(manutencao_id, solucao, custo)

    def registrar_saida(self, manutencao_id: int) -> None:
        self.manutencoes_model.registrar_saida(manutencao_id)

    def listar_pendentes(self):
        return self.manutencoes_model.listar_pendentes()
    
    def listar_em_andamento(self):
        return self.manutencoes_model.listar_em_andamento()
    
    def listar_concluidos(self):
        return self.manutencoes_model.listar_concluidos()
    
    def listar_todas(self):
        return self.manutencoes_model.listar_todas()
    
    def listar_por_patrimonio(self, patrimonio_id):
        return self.manutencoes_model.listar_por_patrimonio(patrimonio_id)
    
    def listar_por_mecanico(self, mecanico_id):
        return self.manutencoes_model.listar_por_mecanico(mecanico_id)