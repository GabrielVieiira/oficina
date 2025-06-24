from models.manutencao_status_model import ManutencaoStatusModel

class ManutencaoStatusService:
    def __init__(self):
        self.model = ManutencaoStatusModel()

    def listar_manutencao_status(self) -> list:
        return self.model.get_manutencao_status()
    
    def status_permitidos_para_criacao(self) -> list:
        manutencao_status = self.listar_manutencao_status()
        return [s for s in manutencao_status if s["nome"] in ["AGUARDANDO PLANEJAMENTO", "INICIADO", "FINALIZADO"]]
    
    def status_selecao(self) -> list[dict]:
        dicionario_nulo = {
            'id': None,
            'nome': ''
        }

        dicionario_todos = {
            'id': 0,
            'nome': 'TODOS'
        }

        manutencao_status = [dicionario_nulo, dicionario_todos] + self.listar_manutencao_status()
        return manutencao_status