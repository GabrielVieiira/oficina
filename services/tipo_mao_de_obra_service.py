from models.tipo_mao_de_obra_model import TipoMaoDeObraModel

class TipoMaoDeObraService:
    def __init__(self):
        self.model = TipoMaoDeObraModel()

    def listar_tipos_mao_de_obra(self) -> list:
        return self.model.get_tipos_mao_de_obra()
    
    def tipos_mao_de_obra_selecao(self) -> list:
        tipos_mao_de_obra = self.listar_tipos_mao_de_obra()
        return [t for t in tipos_mao_de_obra if t["nome"] not in ["AGUARDANDO PLANEJAMENTO", "INICIADO", "FINALIZADO"]]