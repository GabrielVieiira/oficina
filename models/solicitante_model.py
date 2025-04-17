import streamlit as st

from core.database_manager import DatabaseManager

class SolicitantesModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def _existe_solicitante (self, nome: str) -> bool:
        try:
            query = '''SELECT * FROM solicitantes WHERE nome = ?'''
            solicitante = self.fetch_one(query, (nome,))
            if solicitante:
                return True
            else:
                return False
        except Exception as e:
            st.error(f'Erro ao verificar solicitante: {e}')
            return True
    
    def create_solicitante(self, nome: str, regional: int) -> None:
        nome = nome.strip().upper()
        if self._existe_solicitante(nome):
            st.error("Solicitante já cadastrado.")
            return None
        try:
            query = '''INSERT INTO solicitantes (nome, regional_id) VALUES (?, ?)'''
            self.execute_query(query, (nome, regional))
        except Exception as e:
            st.error(f'Erro ao cadastrar solicitante: {e}')
    
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