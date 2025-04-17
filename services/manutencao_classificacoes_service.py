from models.manutencao_classificacao_model import ManutencaoClassificacaoModel

class ManutencaoClassificacoesService:
    def __init__(self):
        self.model = ManutencaoClassificacaoModel()

    def listar_manutencao_classificacoes(self) -> list:
        return self.model.get_manutencao_classificacoes()