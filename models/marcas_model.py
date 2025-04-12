import streamlit as st

from core.database_manager import DatabaseManager

class MarcaModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_marcas(self) -> list:
        try:
            query = 'SELECT * FROM marca'
            marcas = self.fetch_all(query)
            if marcas:
                dados = [{'id': marca[0], 'nome': marca[1]} for marca in marcas]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao recuperar informações de marcas: {e}')
            return []