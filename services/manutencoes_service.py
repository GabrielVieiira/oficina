import datetime

from models.manutencoes_model import ManutencoesModel

class ManutencoesService:
    def __init__(self):
        self.manutencoes_model = ManutencoesModel()

    def registrar_entrada(
            self,
            patrimonio_id: int,
            regional_id: int,
            mecanico_id: int,
            solicitante_id:int,
            classificacao_manutencao_id: int,
            prioridade: str,
            tipo_manutencao: str,
            data_entrada:datetime.date,
            tipo_mao_de_obra: str,
            previsao_termino: datetime.date,
            descricao_manutencao:str
            ) -> None:
        
        self.manutencoes_model.create_manutencao(
            patrimonio_id,
            regional_id,
            mecanico_id,
            solicitante_id,
            classificacao_manutencao_id,
            prioridade,
            tipo_manutencao, data_entrada,
            tipo_mao_de_obra,
            previsao_termino,
            descricao_manutencao
            )

    def iniciar_manutencao(self, manutencao_id: int) -> None:
        self.manutencoes_model.iniciar_manutencao(manutencao_id)

    def concluir_manutencao(self, manutencao_id: int, solucao: str, custo: float) -> None:
        self.manutencoes_model.concluir_manutencao(manutencao_id, solucao, custo)

    def registrar_saida(self, manutencao_id: int) -> None:
        self.manutencoes_model.registrar_saida(manutencao_id)

    def listar_manutencoes(self):
        return self.manutencoes_model.get_all_manutencoes()
    
    def atualizar_manutencao(
        self,
        id: int,
        novo_status: int,
        inicio_manutencao: datetime.date,
        tipo_mao_de_obra: str,
        tipo_manutencao: str,
        nova_descricao: str,
        data_entrada: datetime.date,
        previsao_termino: datetime.date,
        novo_mecanico: int,
        prioridade: str,
        data_termino_manutencao: datetime.date,
    ) -> bool:
        try:
            self.manutencoes_model.atualizar_manutencao(
                id,
                novo_status,
                inicio_manutencao,
                tipo_mao_de_obra,
                tipo_manutencao,
                nova_descricao,
                data_entrada,
                previsao_termino,
                novo_mecanico,
                prioridade,
                data_termino_manutencao
            )
            return True
        except Exception as e:
            print(f"Erro ao atualizar manutenção: {e}")
            return False
    
    def listar_em_andamento(self):
        return self.manutencoes_model.listar_em_andamento()
    
    def listar_concluidos(self):
        return self.manutencoes_model.get_manutencoes_concluidas()
    
    def listar_todas(self):
        return self.manutencoes_model.listar_todas()
    
    def listar_por_patrimonio(self, patrimonio_id):
        return self.manutencoes_model.listar_por_patrimonio(patrimonio_id)
    
    def listar_por_mecanico(self, mecanico_id):
        return self.manutencoes_model.listar_por_mecanico(mecanico_id)