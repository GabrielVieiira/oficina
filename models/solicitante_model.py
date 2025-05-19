from core.database_manager import DatabaseManager

class SolicitantesModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def solicitante_ja_existe (self, nome: str) -> bool:
            query = '''SELECT * FROM solicitantes WHERE nome = ?'''
            solicitante = self.fetch_one(query, (nome,))
            return bool(solicitante)
    
    def create_solicitante(self, nome: str, regional: int) -> None:
        query = '''INSERT INTO solicitantes (nome, regional_id) VALUES (?, ?)'''
        self.execute_query(query, (nome, regional))
    
    def get_solicitantes(self) -> list[dict]:
        query = ''' SELECT
                        solicitantes.id,
                        solicitantes.nome,
                        regionais.nome AS regional
                    FROM solicitantes
                    JOIN regionais ON solicitantes.regional_id = regionais.id'''
        solicitantes = self.fetch_all(query)
        if solicitantes:
            return solicitantes
        else:
            return []
        
    def delete_solicitante(self, id: int) -> None:
        query = '''DELETE FROM solicitantes WHERE id = ?'''
        self.execute_query(query, (id,))