from core.database_manager import DatabaseManager

class PatrimonioClassificacoesModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_patrimonio_classificacoes(self) -> list[dict]:
        query = 'SELECT * FROM patrimonioClassificacao'
        classificacao = self.fetch_all(query)
        if classificacao:
            return classificacao
        else:
            return []