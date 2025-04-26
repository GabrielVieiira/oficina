import streamlit as st

from core.database_manager import DatabaseManager

class SolicitantesModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def solicitante_ja_existe (self, nome: str) -> bool:
        try:
            query = '''SELECT * FROM solicitantes WHERE nome = ?'''
            solicitante = self.fetch_one(query, (nome,))
            return bool(solicitante)
        except Exception as e:
            raise Exception(f'Erro ao verificar solicitante: {e}')
    
    def create_solicitante(self, nome: str, regional: int) -> None:
        try:
            query = '''INSERT INTO solicitantes (nome, regional_id) VALUES (?, ?)'''
            self.execute_query(query, (nome, regional))
        except Exception as e:
            raise Exception(f'Erro ao cadastrar solicitante: {e}')
    
    def get_solicitantes(self) -> list:
        try:
            query = ''' SELECT
                            solicitantes.id,
                            solicitantes.nome,
                            regionais.nome
                        FROM solicitantes
                        JOIN regionais ON solicitantes.regional_id = regionais.id'''
            solicitantes = self.fetch_all(query)
            if solicitantes:
                dados = [{'id': solicitante[0], 'nome': solicitante[1], 'regional': solicitante[2]} for solicitante in solicitantes]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao listar solicitantes: {e}')
            return []