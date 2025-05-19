from models.manutencoes_model import ManutencoesModel
import datetime

class ManutencoesService:
    def __init__(self):
        self.manutencoes_model = ManutencoesModel()

    def _validar_comum(self, **dados):
        obrigatorios = ["patrimonio_id", "regional_id", "solicitante_id", "manutencao_classificacao_id",
                        "prioridade", "tipo_manutencao_id", "dt_entrada",
                        "problema_descricao", "observacao", "status_id", "locais_id", "qtd_horas_mecanico"]
        for campo in obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

    def _validar_planejada(self, **dados):
        self._validar_comum(**dados)

    def _validar_iniciada(self, **dados):
        self._validar_comum(**dados)
        if not dados.get("mecanico_id"):
            raise ValueError("O mecânico responsável deve ser informado.")
        if not dados.get("dt_inicio_manutencao"):
            raise ValueError("A data de início deve ser informada.")
        if dados["dt_inicio_manutencao"] < dados["dt_entrada"]:
            raise ValueError("A data de início não pode ser anterior à data de entrada.")
        if not dados.get("tipo_mao_de_obra_id"):
            raise ValueError("O tipo de mão de obra deve ser informado.")

    def _validar_finalizada(self, **dados):
        self._validar_iniciada(**dados)
        if not dados.get("dt_termino_manutencao"):
            raise ValueError("A data de término da manutenção deve ser informada.")
        if dados["dt_termino_manutencao"] < dados["dt_inicio_manutencao"]:
            raise ValueError("A data de término não pode ser anterior à data de início.")
        if not dados.get("resolucao_do_problema"):
            raise ValueError("A resolução do problema deve ser informada.")

    def _cadastrar_planejada(self, **dados):
        self._validar_planejada(**dados)
        self.manutencoes_model.create_manutencao(**dados)

    def _cadastrar_iniciada(self, **dados):
        self._validar_iniciada(**dados)
        self.manutencoes_model.create_manutencao(**dados)

    def _cadastrar_finalizada(self, **dados):
        self._validar_finalizada(**dados)
        self.manutencoes_model.create_manutencao(**dados)

    def cadastrar_manutencao(self, status_id: int, **dados) -> None:
        handlers = {
            1: self._cadastrar_planejada,
            2: self._cadastrar_iniciada,
            5: self._cadastrar_finalizada
        }

        handler = handlers.get(status_id)
        if not handler:
            raise ValueError(f"Status ID {status_id} não suportado para cadastro.")

        dados["status_id"] = status_id
        handler(**dados)

    def listar_manutencoes(self):
        return self.manutencoes_model.get_all_manutencoes()

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

    def atualizar_manutencao(self, **dados) -> None:

        self.manutencoes_model.atualizar_manutencao(**dados)

    def listar_concluidos(self):
        return self.manutencoes_model.get_manutencoes_concluidas()

    def listar_manutencoes_por_patrimonio(self, patrimonio_id):
        return self.manutencoes_model.get_manutencoes_por_patrimonio(patrimonio_id)

    def excluir_manutencao(self, id: int) -> None:
        self.manutencoes_model.excluir_manutencao(id)

    def manutencoes_iniciadas(self, data_inicio: datetime.date, data_fim: datetime.date) -> list[dict]:
        return self.manutencoes_model.get_manutencoes_iniciadas(data_inicio, data_fim)

    def manutencoes_finalizadas(self, data_inicio: datetime.date, data_fim: datetime.date) -> list[dict]:
        return self.manutencoes_model.get_manutencoes_finalizadas(data_inicio, data_fim)

    def listar_patrimonios_em_manutencao(self) -> list[dict]:
        return self.manutencoes_model.get_patrimonios_em_manutencao()
