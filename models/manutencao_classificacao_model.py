import streamlit as st

from core.database_manager import DatabaseManager

class ManutencaoClassificacaoModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_manutencao_classificacoes(self) -> list:
        try:
            query = 'SELECT * FROM manutencaoClassificacao'
            classificacao = self.fetch_all(query)
            if classificacao:
                dados = [{'id': item[0], 'nome': item[1]} for item in classificacao]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao recuperar informações de classificação: {e}')
            return []