import streamlit as st

from core.database_manager import DatabaseManager

class ManutencaoStatusModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_manutencao_status(self):
        try:
            query = '''SELECT * FROM status'''
            status = self.fetch_all(query)
            if status:
                dados = [{'id': item[0], 'nome': item[1]} for item in status]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao listar status: {e}')