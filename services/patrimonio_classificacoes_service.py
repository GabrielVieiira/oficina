from models.patrimonio_classificacoes_model import PatrimonioClassificacoesModel

class PatrimonioClassificacoesService:
    def __init__(self):
        self.patrimonio_classificacao_model = PatrimonioClassificacoesModel()

    def listar_patrimonio_classificacoes(self) -> list:
        return self.patrimonio_classificacao_model.get_patrimonio_classificacoes() or []