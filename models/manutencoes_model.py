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
        solicitante_id: int,
        manutencao_classificacao_id: int,
        tipo_mao_de_obra_id: int,
        tipo_manutencao_id: int,
        prioridade: str,
        dt_entrada: datetime.date,
        dt_inicio_manutencao: datetime.date = None,
        dt_termino_manutencao: datetime.date = None,
        dt_saida: datetime.date = None,
        mecanico_id: int = None,
        qtd_horas_mecanico: int = None,
        problema_descricao: str = None,
        resolucao_do_problema: str = None,
        observacao: str = None,
        status_id: int = 1,
        locais_id: int = None
    ) -> None:
        query = '''
            INSERT INTO manutencoes (
                patrimonio_id,
                regional_id,
                solicitante_id,
                manutencao_classificacao_id,
                tipo_mao_de_obra_id,
                tipo_manutencao_id,
                prioridade,
                dt_entrada,
                dt_inicio_manutencao,
                dt_termino_manutencao,
                dt_saida,
                mecanico_id,
                qtd_horas_mecanico,
                problema_descricao,
                resolucao_do_problema,
                observacao,
                status_id,
                locais_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        self.execute_query(query, (
            patrimonio_id,
            regional_id,
            solicitante_id,
            manutencao_classificacao_id,
            tipo_mao_de_obra_id,
            tipo_manutencao_id,
            prioridade,
            dt_entrada,
            dt_inicio_manutencao,
            dt_termino_manutencao,
            dt_saida,
            mecanico_id,
            qtd_horas_mecanico,
            problema_descricao,
            resolucao_do_problema,
            observacao,
            status_id,
            locais_id
        ))

    def get_all_manutencoes(self) -> list:
        query = ''' SELECT
                        id,
                        patrimonio_id,
                        regional_id,
                        solicitante_id,
                        manutencao_classificacao_id,
                        tipo_mao_de_obra_id,
                        tipo_manutencao_id,
                        prioridade,
                        dt_entrada,
                        dt_inicio_manutencao,
                        dt_termino_manutencao,
                        qtd_horas_mecanico,
                        problema_descricao,
                        resolucao_do_problema,
                        observacao,
                        status_id,
                        locais_id,
                        mecanico_id
                    FROM manutencoes
                    ORDER BY dt_entrada DESC; '''
        manutencoes = self.fetch_all(query)
        if manutencoes:
            return manutencoes
        else:
            return False

    def atualizar_manutencao(
        self,
        id: int,
        status_id: int,
        patrimonio_id: int,
        regional_id: int,
        solicitante_id: int,
        manutencao_classificacao_id: int,
        prioridade_id: int,
        tipo_manutencao_id: int,
        dt_entrada: datetime.date,
        problema_descricao: datetime.date,
        observacao: str,
        mecanico_id: int,
        dt_inicio_manutencao: datetime.date,
        dt_termino_manutencao: datetime.date,
        tipo_mao_de_obra_id: int,
        qtd_horas_mecanico: int,
        locais_id: int,
        resolucao_do_problema: str
            ) -> None:
        try:
            query = '''UPDATE manutencoes SET
                        status_id = ?,
                        solicitante_id = ?,
                        manutencao_classificacao_id = ?,
                        prioridade = ?,
                        tipo_manutencao_id = ?,
                        dt_entrada = ?,
                        problema_descricao = ?,
                        observacao = ?,
                        mecanico_id = ?,
                        dt_inicio_manutencao = ?,
                        dt_termino_manutencao = ?,
                        tipo_mao_de_obra_id = ?,
                        qtd_horas_mecanico = ?,
                        locais_id= ?,
                        resolucao_do_problema = ?
                    WHERE id = ?'''
            self.execute_query(query, (status_id, solicitante_id, manutencao_classificacao_id, prioridade_id, tipo_manutencao_id, dt_entrada,problema_descricao, observacao, mecanico_id, dt_inicio_manutencao, dt_termino_manutencao, tipo_mao_de_obra_id, qtd_horas_mecanico, locais_id, resolucao_do_problema,id))
        except Exception as e:
            st.error(f'Erro ao atualizar manutenção: {e}')

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

    def get_manutencoes_por_patrimonio(self, patrimonio_id: int) -> list:
        query = ''' SELECT
                        *
                    FROM manutencoes
                    WHERE manutencoes.patrimonio_id = ?;'''
        manutencoes = self.fetch_all(query, (patrimonio_id,))
        if manutencoes:
            return manutencoes
        else:
            return False

    def get_manutencoes_abertas_por_patrimonio(self, patrimonio_id: int):
        manutencoes = self.get_manutencoes_por_patrimonio(patrimonio_id)
        if manutencoes:
            ...

    def excluir_manutencao(self, id: int) -> None:
        query = '''DELETE FROM manutencoes WHERE id = ?'''
        self.execute_query(query, (id,))

    def get_manutencoes_iniciadas(self, data_inicio: datetime, data_fim: datetime) -> list[dict]:
        query = '''
                SELECT
                    m.id,
                    p.numeroPatrimonio AS patrimonio,
                    m.dt_entrada,
                    m.prioridade,
                    s.nome AS status,
                    tm.nome AS tipo_manutencao,
                    mo.nome AS tipo_mao_obra,
                    r.nome AS regional,
                    mc.nome AS classificacao,
                    mec.nome AS mecanico
                FROM manutencoes m
                LEFT JOIN patrimonios p ON m.patrimonio_id = p.id
                LEFT JOIN status s ON m.status_id = s.id
                LEFT JOIN tipoManutencao tm ON m.tipo_manutencao_id = tm.id
                LEFT JOIN tipoMaoDeObra mo ON m.tipo_mao_de_obra_id = mo.id
                LEFT JOIN regionais r ON m.regional_id = r.id
                LEFT JOIN manutencaoClassificacao mc ON m.manutencao_classificacao_id = mc.id
                LEFT JOIN mecanicos mec ON m.mecanico_id = mec.id
                WHERE m.status_id IN (1, 2)  -- Aguardando planejamento ou Iniciada
                AND m.dt_entrada BETWEEN ? AND ?
                ORDER BY m.dt_entrada DESC;
        '''
        return self.fetch_all(query, (data_inicio, data_fim))

    def get_manutencoes_finalizadas(self, data_inicio: datetime, data_fim: datetime) -> list[dict]:
        query = '''
                SELECT
                    m.id,
                    p.numeroPatrimonio AS patrimonio,
                    m.dt_entrada,
                    m.dt_termino_manutencao,
                    m.qtd_horas_mecanico,
                    m.resolucao_do_problema,
                    r.nome AS regional,
                    tm.nome AS tipo_manutencao,
                    s.nome AS status,
                    mec.nome AS mecanico
                FROM manutencoes m
                LEFT JOIN patrimonios p ON m.patrimonio_id = p.id
                LEFT JOIN status s ON m.status_id = s.id
                LEFT JOIN tipoManutencao tm ON m.tipo_manutencao_id = tm.id
                LEFT JOIN regionais r ON m.regional_id = r.id
                LEFT JOIN mecanicos mec ON m.mecanico_id = mec.id
                WHERE m.status_id = 5  -- Finalizada
                AND m.dt_termino_manutencao BETWEEN ? AND ?
                ORDER BY m.dt_termino_manutencao DESC;
        '''
        return self.fetch_all(query, (data_inicio, data_fim))

    def get_patrimonios_em_manutencao(self) -> list[dict]:
        query = '''
            SELECT
                p.numeroPatrimonio AS patrimonio,
                p.modelo,
                r.nome AS regional,
                m.dt_entrada,
                s.nome AS status
            FROM manutencoes m
            LEFT JOIN patrimonios p ON m.patrimonio_id = p.id
            LEFT JOIN regionais r ON m.regional_id = r.id
            LEFT JOIN status s ON m.status_id = s.id
            WHERE m.dt_saida IS NULL
            ORDER BY m.dt_entrada ASC
        '''
        return self.fetch_all(query)
