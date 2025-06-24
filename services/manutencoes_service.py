from models.manutencoes_model import ManutencoesModel
from datetime import datetime, date
from typing import Optional
import pandas as pd

class ManutencoesService:
    def __init__(self):
        self.manutencoes_model = ManutencoesModel()

    def _validar_comum(self, **dados):
        obrigatorios = ['patrimonio_id', 'regional_id', 'solicitante_id', 'classificacao_de_manutencao_id',
                        'prioridade_id', 'tipo_de_manutencao_id', 'dt_entrada',
                        'problema_descricao', 'observacao', 'status_de_manutencao_id', 'localidade_id', 'qtd_horas_mecanico']
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f'O campo "{campo}" é obrigatório.')

    def _validar_planejada(self, **dados):
        self._validar_comum(**dados)

    def _validar_iniciada(self, **dados):
        self._validar_comum(**dados)
        if not dados.get('mecanicos_id'):
            raise ValueError('O mecânico responsável deve ser informado.')
        if not dados.get('dt_inicio_manutencao'):
            raise ValueError('A data de início deve ser informada.')
        if dados['dt_inicio_manutencao'] < dados['dt_entrada']:
            raise ValueError('A data de início não pode ser anterior à data de entrada.')
        if not dados.get('tipo_de_mao_de_obra_id'):
            raise ValueError('O tipo de mão de obra deve ser informado.')

    def _validar_finalizada(self, **dados):
        self._validar_iniciada(**dados)
        if not dados.get('dt_termino_manutencao'):
            raise ValueError('A data de término da manutenção deve ser informada.')
        if dados['dt_termino_manutencao'] < dados['dt_inicio_manutencao']:
            raise ValueError('A data de término não pode ser anterior à data de início.')
        if not dados.get('problema_resolucao'):
            raise ValueError('A resolução do problema deve ser informada.')

    def _cadastrar_planejada(self, **dados):
        self._validar_planejada(**dados)
        dados.pop('mecanicos_id', None)
        self.manutencoes_model.create_manutencao(**dados)
        manutencao_id = self.manutencoes_model.buscar_id_ultima_manutencao(dados['patrimonio_id'])
        if not self._ja_esta_na_oficina(dados['patrimonio_id']):
            self.registrar_entrada_na_oficina(manutencao_id, dados['patrimonio_id'], dados['dt_entrada'])


    def _cadastrar_iniciada(self, **dados):
        self._validar_iniciada(**dados)
        mecanicos_id = dados.pop('mecanicos_id', None)
        self.manutencoes_model.create_manutencao(**dados)
        manutencao_id = self.manutencoes_model.buscar_id_ultima_manutencao(dados['patrimonio_id'])
        if not self._ja_esta_na_oficina(dados['patrimonio_id']):
            self.registrar_entrada_na_oficina(manutencao_id, dados['patrimonio_id'], dados['dt_entrada'])
        self.manutencoes_model.cadastrar_mecanicos(manutencao_id, mecanicos_id)

    def _cadastrar_finalizada(self, **dados):
        self._validar_finalizada(**dados)
        mecanicos_id = dados.pop('mecanicos_id', None)
        self.manutencoes_model.create_manutencao(**dados)
        manutencao_id = self.manutencoes_model.buscar_id_ultima_manutencao(dados['patrimonio_id'])
        self.manutencoes_model.cadastrar_mecanicos(manutencao_id, mecanicos_id)


    def cadastrar_manutencao(self, **dados) -> None:
        handlers = {
            1: self._cadastrar_planejada,
            2: self._cadastrar_iniciada,
            5: self._cadastrar_finalizada
        }

        handler = handlers.get(dados['status_de_manutencao_id'])
        if not handler:
            raise ValueError(f'Status ID {dados["status_de_manutencao_id"]} não suportado para cadastro.')
        handler(**dados)

    def listar_manutencoes(self) -> list[dict]:
        manutencoes = self.manutencoes_model.get_all_manutencoes()
        mecanicos_map = self.manutencoes_model.get_mecanicos_por_manutencao()

        for m in manutencoes:
            m_id = m['id']
            m['mecanicos'] = mecanicos_map.get(m_id, [])
        return manutencoes
    
    def listar_manutencoes_por_status(self, status_selecionado: int) -> list[dict]:
        if status_selecionado is None:
            return []
        elif status_selecionado < 1:
            manutencoes = self.manutencoes_model.get_all_manutencoes()
        else:
            manutencoes = self.manutencoes_model.get_manutencoes_por_status(status_selecionado)
            
        mecanicos_map = self.manutencoes_model.get_mecanicos_por_manutencao()
        for m in manutencoes:
            m_id = m['id']
            m['mecanicos'] = mecanicos_map.get(m_id, [])
        return manutencoes

    def manutencao_selecao(self) -> list:
        try:
            manutencoes = self.manutencoes_model.get_all_manutencoes()
            dicionario_em_branco = {
                        'id': None,
                        'numero_patrimonio': '',
                        'mecanico_nome': '',
                        'regional_nome': '',
                        'solicitante_nome': '',
                        'descricao': '',
                        'tipo_mao_de_obra': '',
                        'cassificacao_manutencao': '',
                        'tipo_manutencao': '',
                        'data_entrada': '',
                        'inicio_manutencao': '',
                        'previsao_termino': '',
                        'termino_manutencao': '',
                        'prioridade': '',
                        'status_nome': '',
                        'no_status_desde': ''
                    }
            if manutencoes:
                return [dicionario_em_branco] + manutencoes
            else:
                return [dicionario_em_branco]
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de manutenção: {e}')

    def atualizar_manutencao(
        self,
        id: int,
        status_de_manutencao_id: int,
        patrimonio_id: int,
        regional_id: int,
        solicitante_id: int,
        classificacao_de_manutencao_id: int,
        prioridade_id: int,
        tipo_de_manutencao_id: int,
        dt_entrada: datetime,
        problema_descricao: Optional[str],
        observacao: Optional[str],
        mecanicos_ids: Optional[list[int]]= None,
        dt_inicio_manutencao: Optional[datetime] = None,
        dt_termino_manutencao: Optional[datetime] = None,
        tipo_de_mao_de_obra_id: Optional[int] = None,
        qtd_horas_mecanico: int = 0,
        localidade_id: Optional[int] = None,
        problema_resolucao: Optional[str] = ''
    ) -> None:
        self.manutencoes_model.atualizar_manutencao(
            id=id,
            status_de_manutencao_id=status_de_manutencao_id,
            patrimonio_id=patrimonio_id,
            regional_id=regional_id,
            solicitante_id=solicitante_id,
            classificacao_de_manutencao_id=classificacao_de_manutencao_id,
            prioridade_id=prioridade_id,
            tipo_de_manutencao_id=tipo_de_manutencao_id,
            dt_entrada=dt_entrada,
            problema_descricao=problema_descricao,
            observacao=observacao,
            dt_inicio_manutencao=dt_inicio_manutencao,
            dt_termino_manutencao=dt_termino_manutencao,
            tipo_de_mao_de_obra_id=tipo_de_mao_de_obra_id,
            qtd_horas_mecanico=qtd_horas_mecanico,
            localidade_id=localidade_id,
            problema_resolucao=problema_resolucao
        )
        if mecanicos_ids is not None:
            self.manutencoes_model.atualizar_mecanicos_da_manutencao(id, mecanicos_ids)

    def listar_concluidos(self):
        return self.manutencoes_model.get_manutencoes_concluidas()

    def listar_manutencoes_por_patrimonio(self, patrimonio_id):
        return self.manutencoes_model.get_manutencoes_por_patrimonio(patrimonio_id)

    def excluir_manutencao(self, id: int) -> None:
        self.manutencoes_model.excluir_manutencao(id)

    def manutencoes_iniciadas(self, data_inicio: date, data_fim: date) -> pd.DataFrame:
        resultados = pd.DataFrame(self.manutencoes_model.get_manutencoes_iniciadas(data_inicio, data_fim))

        if 'dt_entrada' in resultados.columns:
            resultados['dt_entrada'] = pd.to_datetime(resultados['dt_entrada']).dt.strftime('%d/%m/%Y')

        return resultados

    def manutencoes_finalizadas(self, data_inicio: date, data_fim: date) -> pd.DataFrame:
        resultados = pd.DataFrame(self.manutencoes_model.get_manutencoes_finalizadas(data_inicio, data_fim))
        
        if 'dt_entrada' in resultados.columns:
            resultados['dt_entrada'] = pd.to_datetime(resultados['dt_entrada']).dt.strftime('%d/%m/%Y')
        if 'dt_termino_manutencao' in resultados.columns:
            resultados['dt_termino_manutencao'] = pd.to_datetime(resultados['dt_termino_manutencao']).dt.strftime('%d/%m/%Y')
            
        return resultados

    def listar_patrimonios_na_oficina(self) -> list:
        resultados = self.manutencoes_model.get_patrimonios_na_oficina() or []
        for patrimonio in resultados:
            data = patrimonio.get('dt_entrada')

            if isinstance(data, str):
                try:
                    data_obj = datetime.strptime(data, '%Y-%m-%d')
                    patrimonio['dt_entrada'] = data_obj.strftime('%d/%m/%Y')
                except ValueError:
                    # Mantém o valor original caso já esteja no formato desejado
                    pass
            elif isinstance(data, (datetime, datetime)):
                patrimonio['dt_entrada'] = data.strftime('%d/%m/%Y')
            else:
                patrimonio['dt_entrada'] = ''

        return resultados
    
    def registrar_entrada_na_oficina(self, manutencao_id: int, patrimonio_id: int, dt_entrada: datetime) -> None:
        self.manutencoes_model.registrar_entrada_na_oficina(manutencao_id, patrimonio_id, dt_entrada)
    
    def registrar_retirada_da_oficina(self, patrimonio_id: int) -> None:
        self.manutencoes_model.registrar_retirada_da_oficina(patrimonio_id)
        
    def _ja_esta_na_oficina(self, patrimonio_id: int) -> bool:
        return self.manutencoes_model.ja_esta_na_oficina(patrimonio_id)

    def registrar_saida_da_oficina(self, manutencao_id: int, data_saida: date) -> None:
        self.manutencoes_model.registrar_saida(manutencao_id, data_saida)
        
    def listar_veiculos_por_status_de_manutencao(self, status_de_manutencao_id: int) -> list[dict]:
        dicionario_em_branco =[{
            'patrimonio_id': None,
            'patrimonio_numero': '',
        }]
        if status_de_manutencao_id is None:
            return dicionario_em_branco
        return dicionario_em_branco + self.manutencoes_model.get_veiculos_por_status_de_manutencao(status_de_manutencao_id)
    
    def listar_manutencoes_por_status_e_patrimonio(self, status_de_manutencao_id: int, patrimonio_id: int) -> list[dict]:
        if status_de_manutencao_id is None or patrimonio_id is None :
            return []
        elif status_de_manutencao_id < 1:
            return self.manutencoes_model.get_all_manutencoes_por_patrimonio(patrimonio_id)
        else:
            return self.manutencoes_model.get_manutencoes_por_status_e_patrimonio(status_de_manutencao_id, patrimonio_id)