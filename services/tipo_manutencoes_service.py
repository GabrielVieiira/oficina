from models.tipo_manutencoes_model import TipoManutencaoModel

class TipoManutencaoService:
    def __init__(self):
        self.model = TipoManutencaoModel()

    def listar_tipos_manutencao(self) -> list:
        return self.model.get_tipos_manutencao()
    
    def tipos_manutencao_selecao(self) -> list:
        tipos_manutencao = self.listar_tipos_manutencao()
        return [t for t in tipos_manutencao if t["nome"] not in ["AGUARDANDO PLANEJAMENTO", "INICIADO", "FINALIZADO"]]