import streamlit as st

from core.database_manager import DatabaseManager

class PatrimoniosModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_patrimonio(self) -> list[dict]:
        query = ''' SELECT 
                            patrimonios.id,
                            patrimonios.numero_do_patrimonio,
                            centros_de_custo.nome as centroDeCusto,
                            patrimonios.modelo,
                            classificacoes_de_patrimonios.nome AS classificacao,
                            patrimonios.proprio
                    FROM patrimonios
                    LEFT JOIN centros_de_custo ON patrimonios.centro_de_custo_id = centros_de_custo.id
                    LEFT JOIN classificacoes_de_patrimonios on patrimonios.classificacao_id = classificacoes_de_patrimonios.id '''
        patrimonios = self.fetch_all(query)
        if patrimonios:
            return patrimonios
        else:
            return []
        
    def get_patrimonio_by_id(self, id: int) -> dict:
        query = f'SELECT * FROM patrimonios WHERE id = {id}'
        patrimonio = self.fetch_one(query)
        if patrimonio:
            return patrimonio
        else:
            return {}
        
    def patrimonio_ja_existe(self, numero: str) -> bool:
        query = f'SELECT * FROM patrimonios WHERE numero_do_patrimonio = ?'
        patrimonio = self.fetch_one(query, (numero,))
        return bool(patrimonio)
    
    def create_patrimonio(
        self,
        numero: str,
        centro_de_custo_id: int,
        modelo: str,
        classificacao_id: int,
        proprio: bool
    ) -> None:
        query = '''
            INSERT INTO patrimonios (
                numero_do_patrimonio,
                centro_de_custo_id,
                modelo,
                classificacao_id,
                proprio
            ) VALUES (?, ?, ?, ?, ?)
        '''
        params = (
            numero,
            centro_de_custo_id,
            modelo,
            classificacao_id,
            proprio
        )
        self.execute_query(query, params)
        
    def delete_patrimonio(self, id: int) -> None:
        query = 'DELETE FROM patrimonios WHERE id = ?'
        params = (id,)
        self.execute_query(query, params)