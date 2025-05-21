from core.database_manager import DatabaseManager


class TipoManutencaoModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def tipo_manutencao_ja_existe(self, nome: str) -> bool:
        query = '''SELECT * FROM tipo_de_manutencoes WHERE nome = ?'''
        tipo_manutencao = self.fetch_one(query, (nome,))
        return bool(tipo_manutencao)

    def create_tipo_manutencao(self, nome: str) -> None:
        query = '''INSERT INTO tipo_de_manutencoes (nome) VALUES (?)'''
        self.execute_query(query, (nome,))
        
    def get_tipos_manutencao(self) -> list[dict]:
        query = '''SELECT * FROM tipo_de_manutencoes'''
        tipos_manutencao = self.fetch_all(query)
        if tipos_manutencao:
            return tipos_manutencao
        else:
            return []