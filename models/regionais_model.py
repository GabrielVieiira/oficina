from core.database_manager import DatabaseManager

class RegionalModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_regional(self) -> list[dict]:
        query = 'SELECT * FROM regionais'
        regionais = self.fetch_all(query)
        if regionais:
            return regionais
        else:
            return []