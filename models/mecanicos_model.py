import streamlit as st

from core.database_manager import DatabaseManager

class MecanicosModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_mecanico(self) -> list[dict]:
        query = ''' SELECT 
                        mecanicos.id,
                        mecanicos.nome,
                        cargos.nome AS cargo,
                        regionais.nome AS regional
                    FROM mecanicos
                    JOIN cargos ON mecanicos.cargo_id = cargos.id
                    JOIN regionais ON mecanicos.regional_id = regionais.id;
                    '''
        mecanicos = self.fetch_all(query)
        if mecanicos:
            return mecanicos
        else:
            return []

    def get_mecanico_by_id(self, id: int) -> dict:
        query = f'SELECT * FROM mecanico WHERE id = {id}'
        mecanico = self.fetch_one(query)
        if mecanico:
            return mecanico
        else:
            return {}
        
    def mecanico_ja_existe(self, nome: str) -> bool:
        query = '''SELECT * FROM mecanicos WHERE nome = ?'''
        mecanico = self.fetch_one(query, (nome,))
        return bool(mecanico)
    
    def create_mecanico(self, nome: str, cargo_id: int, regional_id: int) -> None:
        query = '''INSERT INTO mecanicos (nome, cargo_id, regional_id) VALUES (?, ?, ?)'''
        self.execute_query(query, (nome, cargo_id, regional_id))

        
    def get_cargos(self,) -> list[dict]:
        query = 'SELECT * FROM cargos'
        cargos = self.fetch_all(query)
        if cargos:
            return cargos
        else:
            return []
        
    def delete_mecanico(self, id: int) -> None:
        query = '''DELETE FROM mecanicos WHERE id = ?'''
        self.execute_query(query, (id,))