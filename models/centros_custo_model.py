import streamlit as st

from core.database_manager import DatabaseManager


class CentroCustoModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_centros_custo(self) -> list:
        try:
            query = 'SELECT * FROM centroDeCusto'
            centros_custo = self.fetch_all(query)
            if centros_custo:
                dados = [{'id': centro[0], 'nome': centro[1]} for centro in centros_custo]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao recuperar informações de centro de custo: {e}')
            return []