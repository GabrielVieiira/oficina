from core.database_manager import DatabaseManager

class ManutencaoStatusModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_manutencao_status(self):
        query = '''SELECT * FROM status'''
        manutencoes_status = self.fetch_all(query)
        if manutencoes_status:
            return manutencoes_status
        else:
            return []