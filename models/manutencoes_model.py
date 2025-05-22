import streamlit as st
import datetime
from typing import Optional

from core.database_manager import DatabaseManager

class ManutencoesModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def manutencao_ja_existe(self, patrimonio_id: int) -> bool:
        try:
            query = '''SELECT * FROM manutencoes WHERE patrimonio_id = ? AND status_de_manutencao_id = 1'''
            manutencao = self.fetch_one(query, (patrimonio_id,))
            return bool(manutencao)
        except Exception as e:
            raise Exception(f'Erro ao verificar manutenção: {e}')

    def create_manutencao(
        self,
        patrimonio_id: int,
        regional_id: int,
        solicitante_id: int,
        classificacao_de_manutencao_id: int,
        tipo_de_mao_de_obra_id: int,
        tipo_de_manutencao_id: int,
        prioridade_id: str,
        dt_entrada: datetime.date,
        status_de_manutencao_id: int,
        qtd_horas_mecanico: int,
        problema_descricao: str,
        observacao: str,
        localidade_id: int,
        dt_inicio_manutencao: Optional[datetime.date] = None,
        dt_termino_manutencao: Optional[datetime.date]  = None,
        dt_saida: Optional[datetime.date] = None,
        problema_resolucao: Optional[str] = None,
    ) -> None:
        query = '''
            INSERT INTO manutencoes (
                patrimonio_id,
                regional_id,
                solicitante_id,
                classificacao_de_manutencao_id,
                tipo_de_mao_de_obra_id,
                tipo_de_manutencao_id,
                prioridade_id,
                dt_entrada,
                dt_inicio_manutencao,
                dt_termino_manutencao,
                dt_saida,
                qtd_horas_mecanico,
                problema_descricao,
                problema_resolucao,
                observacao,
                status_de_manutencao_id,
                localidade_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        self.execute_query(query, (
            patrimonio_id,
            regional_id,
            solicitante_id,
            classificacao_de_manutencao_id,
            tipo_de_mao_de_obra_id,
            tipo_de_manutencao_id,
            prioridade_id,
            dt_entrada,
            dt_inicio_manutencao,
            dt_termino_manutencao,
            dt_saida,
            qtd_horas_mecanico,
            problema_descricao,
            problema_resolucao,
            observacao,
            status_de_manutencao_id,
            localidade_id
        ))

    def get_all_manutencoes(self) -> list[dict]:
        query = '''
            SELECT
                id,
                patrimonio_id,
                regional_id,
                solicitante_id,
                classificacao_de_manutencao_id,
                tipo_de_mao_de_obra_id,
                tipo_de_manutencao_id,
                prioridade_id,
                dt_entrada,
                dt_inicio_manutencao,
                dt_termino_manutencao,
                dt_saida,
                qtd_horas_mecanico,
                problema_descricao,
                problema_resolucao,
                observacao,
                status_de_manutencao_id,
                dt_ultima_atualizacao,
                localidade_id
            FROM manutencoes
            ORDER BY dt_entrada DESC;
        '''
        return self.fetch_all(query) or []
    def get_mecanicos_por_manutencao(self) -> dict[int, list[int]]:
        query = '''
            SELECT manutencao_id, mecanico_id
            FROM manutencoes_mecanicos
        '''
        rows = self.fetch_all(query) or []
        mecanicos_por_manutencao = {}
        for row in rows:
            m_id = row['manutencao_id']
            if m_id not in mecanicos_por_manutencao:
                mecanicos_por_manutencao[m_id] = []
            mecanicos_por_manutencao[m_id].append(row['mecanico_id'])
        return mecanicos_por_manutencao

    def atualizar_manutencao(self, **kwargs):
        query = '''
            UPDATE manutencoes SET
                status_de_manutencao_id = ?,
                patrimonio_id = ?,
                regional_id = ?,
                solicitante_id = ?,
                classificacao_de_manutencao_id = ?,
                prioridade_id = ?,
                tipo_de_manutencao_id = ?,
                dt_entrada = ?,
                problema_descricao = ?,
                observacao = ?,
                dt_inicio_manutencao = ?,
                dt_termino_manutencao = ?,
                tipo_de_mao_de_obra_id = ?,
                qtd_horas_mecanico = ?,
                localidade_id = ?,
                problema_resolucao = ?,
                dt_ultima_atualizacao = CURRENT_DATE
            WHERE id = ?
        '''
        params = (
            kwargs['status_de_manutencao_id'],
            kwargs['patrimonio_id'],
            kwargs['regional_id'],
            kwargs['solicitante_id'],
            kwargs['classificacao_de_manutencao_id'],
            kwargs['prioridade_id'],
            kwargs['tipo_de_manutencao_id'],
            kwargs['dt_entrada'],
            kwargs['problema_descricao'],
            kwargs['observacao'],
            kwargs.get('dt_inicio_manutencao'),
            kwargs.get('dt_termino_manutencao'),
            kwargs.get('tipo_de_mao_de_obra_id'),
            kwargs['qtd_horas_mecanico'],
            kwargs.get('localidade_id'),
            kwargs.get('problema_resolucao'),
            kwargs['id']
        )
        self.execute_query(query, params)

    def get_manutencoes_concluidas(self) -> list:
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

    def get_manutencoes_por_patrimonio(self, patrimonio_id: int) -> list[dict]:
        query = ''' SELECT
                        *
                    FROM manutencoes
                    WHERE manutencoes.patrimonio_id = ?;'''
        manutencoes = self.fetch_all(query, (patrimonio_id,))
        if manutencoes:
            return manutencoes
        else:
            return []

    def get_manutencoes_abertas_por_patrimonio(self, patrimonio_id: int):
        manutencoes = self.get_manutencoes_por_patrimonio(patrimonio_id)
        if manutencoes:
            ...

    def excluir_manutencao(self, id: int) -> None:
        query = '''DELETE FROM manutencoes WHERE id = ?'''
        self.execute_query(query, (id,))

    def get_manutencoes_iniciadas(self, data_inicio: datetime.date, data_fim: datetime.date) -> list[dict]:
        query = '''
                SELECT
                    m.id,
                    p.numero_do_patrimonio AS patrimonio,
                    m.dt_entrada,
                    m.prioridade_id,
                    s.nome AS status,
                    tm.nome AS tipo_manutencao,
                    mo.nome AS tipo_mao_obra,
                    r.nome AS regional,
                    mc.nome AS classificacao
                FROM manutencoes m
                LEFT JOIN patrimonios p ON m.patrimonio_id = p.id
                LEFT JOIN status_de_manutencao s ON m.status_de_manutencao_id = s.id
                LEFT JOIN tipo_de_manutencoes tm ON m.tipo_de_manutencao_id = tm.id
                LEFT JOIN tipo_de_mao_de_obra mo ON m.tipo_de_mao_de_obra_id = mo.id
                LEFT JOIN regionais r ON m.regional_id = r.id
                LEFT JOIN classificacoes_de_manutencao mc ON m.classificacao_de_manutencao_id = mc.id
                WHERE m.status_de_manutencao_id IN (1, 2)  -- Aguardando planejamento ou Iniciada
                AND m.dt_entrada BETWEEN ? AND ?
                ORDER BY m.dt_entrada DESC;
        '''
        manutencoes_iniciadas = self.fetch_all(query, (data_inicio, data_fim))
        if manutencoes_iniciadas:
            return self.fetch_all(query, (data_inicio, data_fim))
        else:
            return []

    def get_manutencoes_finalizadas(self, data_inicio: datetime.date, data_fim: datetime.date) -> list[dict]:
        query = '''
                SELECT
                    m.id,
                    p.numero_do_patrimonio AS patrimonio,
                    m.dt_entrada,
                    m.dt_termino_manutencao,
                    m.qtd_horas_mecanico,
                    m.problema_resolucao,
                    r.nome AS regional,
                    tm.nome AS tipo_manutencao,
                    s.nome AS status
                FROM manutencoes m
                LEFT JOIN patrimonios p ON m.patrimonio_id = p.id
                LEFT JOIN status_de_manutencao s ON m.status_de_manutencao_id = s.id
                LEFT JOIN tipo_de_manutencoes tm ON m.tipo_de_manutencao_id = tm.id
                LEFT JOIN regionais r ON m.regional_id = r.id
                WHERE m.status_de_manutencao_id = 5  -- Finalizada
                AND m.dt_termino_manutencao BETWEEN ? AND ?
                ORDER BY m.dt_termino_manutencao DESC;
        '''
        manutencoes_finalizadas = self.fetch_all(query, (data_inicio, data_fim))
        if manutencoes_finalizadas:
            return self.fetch_all(query, (data_inicio, data_fim))
        else:
            return []

    def get_patrimonios_em_manutencao(self) -> list[dict]:
        query = '''
            SELECT
                p.numero_do_patrimonio AS patrimonio,
                p.modelo,
                r.nome AS regional,
                m.dt_entrada,
                s.nome AS status
            FROM manutencoes m
            LEFT JOIN patrimonios p ON m.patrimonio_id = p.id
            LEFT JOIN regionais r ON m.regional_id = r.id
            LEFT JOIN status_de_manutencao s ON m.status_de_manutencao_id = s.id
            WHERE m.dt_saida IS NULL
            ORDER BY m.dt_entrada ASC
        '''
        patrimonios_em_manutencao = self.fetch_all(query)
        if patrimonios_em_manutencao:
            return patrimonios_em_manutencao
        else:
            return []

    def buscar_id_ultima_manutencao(self, patrimonio_id: int) -> int:
        query = '''SELECT max(id) AS id FROM manutencoes WHERE patrimonio_id = ?'''
        manutencao = self.fetch_one(query, (patrimonio_id,))
        return manutencao['id']

    def cadastrar_mecanicos(self, manutencao_id: int, mecanicos_id: list[int]) -> None:
        for mecanico_id in mecanicos_id:
            query = '''INSERT INTO manutencoes_mecanicos (manutencao_id, mecanico_id) VALUES (?, ?)'''
            self.execute_query(query, (manutencao_id, mecanico_id))

    def atualizar_mecanicos_da_manutencao(self, manutencao_id: int, mecanicos_ids: list[int]) -> None:
        # Remove todos os registros atuais
        delete_query = 'DELETE FROM manutencoes_mecanicos WHERE manutencao_id = ?'
        self.execute_query(delete_query, (manutencao_id,))

        # Insere os novos
        insert_query = 'INSERT INTO manutencoes_mecanicos (manutencao_id, mecanico_id) VALUES (?, ?)'
        for mecanico_id in mecanicos_ids:
            self.execute_query(insert_query, (manutencao_id, mecanico_id))
