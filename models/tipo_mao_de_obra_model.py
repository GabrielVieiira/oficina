from core.database_manager import DatabaseManager

class TipoMaoDeObraModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def tipo_mao_de_obra_ja_existe(self, nome: str) -> bool:
        query = '''SELECT * FROM tipo_de_mao_de_obra WHERE nome = ?'''
        tipo_mao_de_obra = self.fetch_one(query, (nome,))
        return bool(tipo_mao_de_obra)

    def create_tipo_mao_de_obra(self, nome: str) -> None:
        query = '''INSERT INTO tipo_de_mao_de_obra (nome) VALUES (?)'''
        self.execute_query(query, (nome,))
        
    def get_tipos_mao_de_obra(self) -> list[dict]:
        query = '''SELECT * FROM tipo_de_mao_de_obra'''
        tipos_mao_de_obra = self.fetch_all(query)
        if tipos_mao_de_obra:
            return tipos_mao_de_obra
        else:
            return []