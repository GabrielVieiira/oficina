import streamlit as st
import datetime

from core.database_manager import DatabaseManager

class ManutencoesModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def manutencao_ja_existe(self, patrimonio_id: int) -> bool:
        try:
            query = '''SELECT * FROM manutencoes WHERE patrimonio_id = ? AND status_id = 1'''
            manutencao = self.fetch_one(query, (patrimonio_id,))
            return bool(manutencao)
        except Exception as e:
            raise Exception(f'Erro ao verificar manutenção: {e}')
    
    def create_manutencao(
            self,
            patrimonio_id: int,
            regional_id: int,
            solicitante_id:int,
            classificacao_manutencao_id: int,
            prioridade: str,
            tipo_manutencao: str,
            data_entrada:datetime.date,
            descricao_problema:str,
            observacao:str,
            ) -> None:
        try:
            query = '''INSERT INTO manutencoes2 (patrimonio_id, regional_id, solicitante_id, manutencaoClassificacao_id, prioridade, tipoManutencao, dtEntrada, problemaDescricao, observacao) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            self.execute_query(
                query,(
                    patrimonio_id,
                    regional_id,
                    solicitante_id,
                    classificacao_manutencao_id,
                    prioridade,
                    tipo_manutencao,
                    data_entrada,
                    descricao_problema,
                    observacao,
                    )
            )
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

    def get_all_manutencoes(self) -> list:
        try:
            query = ''' SELECT 
                            m.id AS manutencao_id,
                            p.numeroPatrimonio AS patrimonio,
                            mc.nome AS mecanico,
                            r.nome AS regional,
                            s.nome AS solicitante,
                            m.descricao,
                            m.tipo_mao_de_obra,
                            mc2.nome AS classificacao_manutencao,
                            m.tipo_manutecao,
                            m.data_entrada,
                            m.inicio_manutencao,
                            m.previsao_termino,
                            m.termino_manutencao,
                            m.prioridade,
                            st.nome AS status,
                            m.no_status_desde
                        FROM manutencoes m
                        JOIN patrimonios p ON m.patrimonio_id = p.id
                        JOIN mecanicos mc ON m.mecanico_id = mc.id
                        JOIN regionais r ON m.regional_id = r.id
                        JOIN solicitantes s ON m.solicitante_id = s.id
                        JOIN manutencaoClassificacao mc2 ON m.manutencao_classificacao_id = mc2.id
                        JOIN status st ON m.status_id = st.id; '''
            manutencoes = self.fetch_all(query)
            if manutencoes:
                return [{'id':manutencao[0],
                         'numero_patrimonio':manutencao[1],
                         'mecanico_nome':manutencao[2],
                         'regional_nome':manutencao[3],
                         'solicitante_nome':manutencao[4],
                         'descricao':manutencao[5],
                         'tipo_mao_de_obra':manutencao[6],
                         'cassificacao_manutencao':manutencao[7],
                         'tipo_manutencao':manutencao[8],
                         'data_entrada':manutencao[9],
                         'inicio_manutencao':manutencao[10],
                         'previsao_termino':manutencao[11],
                         'termino_manutencao':manutencao[12],
                         'prioridade':manutencao[13],
                         'status_nome':manutencao[14],
                         'no_status_desde':manutencao[15]} for manutencao in manutencoes]
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao listar pendências: {e}')
            return []
        
    def atualizar_manutencao(
        self,
        id: int,
        novo_status: int,
        inicio_manutencao: datetime.date,
        tipo_mao_de_obra: str,
        tipo_manutencao: str,
        nova_descricao: str,
        data_entrada: datetime.date,
        previsao_termino: datetime.date,
        novo_mecanico: int,
        prioridade: str,
        data_termino_manutencao: datetime.date,
    ) -> None:
        try:
            query = '''UPDATE manutencoes SET 
                        status_id = ?,
                        inicio_manutencao = ?,
                        tipo_mao_de_obra = ?,
                        tipo_manutecao = ?,
                        descricao = ?,
                        data_entrada = ?,
                        previsao_termino = ?,
                        mecanico_id = ?,
                        prioridade = ?,
                        termino_manutencao = ?
                    WHERE id = ?'''
            self.execute_query(query, (novo_status, inicio_manutencao, tipo_mao_de_obra, tipo_manutencao, nova_descricao, data_entrada, previsao_termino, novo_mecanico, prioridade,data_termino_manutencao, id))
        except Exception as e:
            st.error(f'Erro ao atualizar manutenção: {e}') 
            
    def get_manutencoes_concluidas(self):
        try:
            query = ''' SELECT
                            patrimonios.numeroPatrimonio,
                            status.nome,
                            manutencoes.termino_manutencao
                        FROM manutencoes
                        JOIN status on status.id = manutencoes.status_id
                        JOIN patrimonios on manutencoes.patrimonio_id = patrimonios.id
                        WHERE status.nome = 'FINALIZADO';'''
            manutencoes = self.fetch_all(query)
            if manutencoes:
                return [{'numero_patrimonio': manutencao[0], 'status_nome': manutencao[1], 'termino_manutencao':manutencao[2]} for manutencao in manutencoes]
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao listar pendências: {e}')
            return []
            