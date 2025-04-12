import streamlit as st

from core.database_manager import DatabaseManager

class RegionalModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_regional(self) -> list:
        try:
            query = 'SELECT * FROM regionais'
            regionais = self.fetch_all(query)
            if regionais:
                dados = [{'id':regional[0], 'nome':regional[1]} for regional in regionais]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao recuperar informações de regional: {e}')
            return []