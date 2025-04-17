from models.patrimonio_classificacoes_model import PatrimonioClassificacoesModel

class PatrimonioClassificacoesService:
    def __init__(self):
        self.patrimonio_classificacao_model = PatrimonioClassificacoesModel()

    def listar_patrimonio_classificacoes(self) -> list:
        try:
            classificacoes = self.patrimonio_classificacao_model.get_patrimonio_classificacoes()
            if classificacoes:
                return classificacoes
            else:
                return []
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de classificações: {e}')