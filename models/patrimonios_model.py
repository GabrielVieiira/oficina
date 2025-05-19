import streamlit as st

from core.database_manager import DatabaseManager

class PatrimoniosModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_patrimonio(self) -> list[dict]:
        query = ''' SELECT 
                            patrimonios.id,
                            patrimonios.numeroPatrimonio,
                            centroDeCusto.nome as centroDeCusto,
                            patrimonios.modelo,
                            patrimonioClassificacao.nome AS classificacao,
                            patrimonios.proprio
                    FROM patrimonios
                    LEFT JOIN centroDeCusto ON patrimonios.centroDeCusto_id = centroDeCusto.id
                    LEFT JOIN patrimonioClassificacao on patrimonios.classificacao_id = patrimonioClassificacao.id '''
        patrimonios = self.fetch_all(query)
        if patrimonios:
            return patrimonios
        else:
            return []
        
    def get_patrimonio_by_id(self, id: int) -> dict:
        query = f'SELECT * FROM patrimonio WHERE id = {id}'
        patrimonio = self.fetch_one(query)
        if patrimonio:
            return patrimonio
        else:
            return {}
        
    def patrimonio_ja_existe(self, numero: str) -> bool:
        query = f'SELECT * FROM patrimonios WHERE numeroPatrimonio = ?'
        patrimonio = self.fetch_one(query, (numero,))
        return bool(patrimonio)
        
    def _get_data_atual(self) -> str:
        try:
            query = 'SELECT datetime("now")'
            data = self.fetch_one(query)
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            st.error(f'Erro ao recuperar data atual: {e}')
            return None
    
    def create_patrimonio(
        self,
        numero: str,
        centro_de_custo_id: int,
        modelo: str,
        classificacao_id: int,
        proprio: bool
    ) -> None:
        query = """
            INSERT INTO patrimonios (
                numeroPatrimonio,
                centroDeCusto_id,
                modelo,
                classificacao_id,
                proprio
            ) VALUES (?, ?, ?, ?, ?)
        """
        params = (
            numero,
            centro_de_custo_id,
            modelo,
            classificacao_id,
            proprio
        )
        self.execute_query(query, params)
        
    def delete_patrimonio(self, id: int) -> None:
        query = "DELETE FROM patrimonios WHERE id = ?"
        params = (id,)
        self.execute_query(query, params)