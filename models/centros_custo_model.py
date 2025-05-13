from core.database_manager import DatabaseManager

class CentroCustoModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_centros_custo(self) -> list:
        query = 'SELECT * FROM centroDeCusto'
        centros_custo = self.fetch_all(query)
        if centros_custo:
            return centros_custo
        else:
            return False