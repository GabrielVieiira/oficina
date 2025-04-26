from models.manutencao_classificacao_model import ManutencaoClassificacaoModel

class ManutencaoClassificacoesService:
    def __init__(self):
        self.model = ManutencaoClassificacaoModel()

    def listar_manutencao_classificacoes(self) -> list:
        return self.model.get_manutencao_classificacoes()
    
    def manutencao_classificacoes_selecao(self) -> list:
        try:
            classificacoes = self.model.get_manutencao_classificacoes()
            dicionario_em_branco = {
                'id': None, 
                'nome': ''
            }
            if classificacoes:
                return [dicionario_em_branco] + classificacoes
            else:
                return [dicionario_em_branco]
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de classificações de manutenção: {e}')