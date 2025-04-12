import streamlit as st

from core.database_manager import DatabaseManager

class ManutencoesModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def registrar_entrada(self, patrimonio_id: int, mecanico_id: int, problema: str) -> None:
        try:
            query = '''INSERT INTO manutencoes (patrimonio_id, mecanico_id, problema, dataEntrada) 
                       VALUES (?, ?, ?, ?)'''
            self.execute_query(query, (patrimonio_id, mecanico_id, problema, self.get_current_date()))
        except Exception as e:
            st.error(f'Erro ao registrar entrada: {e}')

    def iniciar_manutencao(self, manutencao_id: int) -> None:
        try:
            query = '''UPDATE manutencoes SET status = 'em_andamento' WHERE id = ?'''
            self.execute_query(query, (manutencao_id,))
        except Exception as e:
            st.error(f'Erro ao iniciar manutenção: {e}')

    def concluir_manutencao(self, manutencao_id: int, solucao: str, custo: float) -> None:
        try:
            query = '''UPDATE manutencoes SET status = 'concluido', solucao = ?, custo = ? WHERE id = ?'''
            self.execute_query(query, (solucao, custo, manutencao_id))
        except Exception as e:
            st.error(f'Erro ao concluir manutenção: {e}')

    def registrar_saida(self, manutencao_id: int) -> None:
        try:
            query = '''UPDATE manutencoes SET status = 'entregue', dataSaida = ? WHERE id = ?'''
            self.execute_query(query, (self.get_current_date(), manutencao_id))
        except Exception as e:
            st.error(f'Erro ao registrar saída: {e}')

    def listar_pendentes(self) -> list:
        try:
            query = '''SELECT * FROM manutencoes WHERE status = 'pendente' '''
            pendentes = self.fetch_all(query)
            if pendentes:
                return pendentes
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao listar pendências: {e}')
            return []