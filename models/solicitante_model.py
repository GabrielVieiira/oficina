import streamlit as st

from core.database_manager import DatabaseManager

class SolicitantesModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def cadastrar_solicitante(self, nome: str, cargo: str, regional: str) -> None:
        try:
            query = '''INSERT INTO solicitantes (nome, cargo, regional) VALUES (?, ?, ?)'''
            self.execute_query(query, (nome, cargo, regional))
        except Exception as e:
            st.error(f'Erro ao cadastrar solicitante: {e}')

    def listar_solicitantes(self) -> list:
        try:
            query = '''SELECT * FROM solicitantes'''
            solicitantes = self.fetch_all(query)
            if solicitantes:
                dados = [{'id': solicitante[0], 'nome': solicitante[1], 'cargo': solicitante[2], 'regional': solicitante[3]} for solicitante in solicitantes]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao listar solicitantes: {e}')
            return []