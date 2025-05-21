from core.database_manager import DatabaseManager

class PrioridadesModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_prioridades(self) -> list[dict]:
        query = ''' SELECT 
                        prioridades.id,
                        prioridades.nome,
                        prioridades.tempo_estimado
                    FROM prioridades '''
        prioridades = self.fetch_all(query)
        if prioridades:
            return prioridades
        else:
            return []