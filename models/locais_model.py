import streamlit as st
from core.database_manager import DatabaseManager

class LocaisModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_locais(self) -> list[dict]:
        query = ''' SELECT 
                        localidades.id,
                        localidades.nome,
                        regionais.nome AS regional
                    FROM localidades
                    JOIN regionais ON localidades.regional_id = regionais.id;
                    '''
        locais = self.fetch_all(query)
        if locais:
            return locais
        else:
            return []
        
    def local_ja_existe(self, nome: str) -> bool:
        query = '''SELECT COUNT(*) FROM localidades WHERE nome = ?'''
        result = self.fetch_one(query, (nome,))
        return result[0] > 0
    
    def create_local(self, nome: str, regional_id: int) -> None:
        query = '''INSERT INTO localidades (nome, regional_id) VALUES (?, ?)'''
        self.execute_query(query, (nome, regional_id))