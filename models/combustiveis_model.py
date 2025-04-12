import streamlit as st

from core.database_manager import DatabaseManager

class CombustiveisModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_combustiveis(self) -> list:
        try:
            query = 'SELECT * FROM combustivel'
            combustiveis = self.fetch_all(query)
            if combustiveis:
                dados = [{'id': combustivel[0], 'nome': combustivel[1]} for combustivel in combustiveis]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao recuperar informações de combustíveis: {e}')
            return []