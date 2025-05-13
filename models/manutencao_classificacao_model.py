from core.database_manager import DatabaseManager

class ManutencaoClassificacaoModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_manutencao_classificacoes(self) -> list:
        query = 'SELECT * FROM manutencaoClassificacao'
        classificacoes = self.fetch_all(query)
        if classificacoes:
            return classificacoes
        else:
            return False