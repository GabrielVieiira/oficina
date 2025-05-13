from models.regionais_model import RegionalModel

class RegionaisService:
    def __init__(self):
        self.reginal_model = RegionalModel()

    def listar_regionais(self) -> list:
        return self.reginal_model.get_regional() or []
    
    def regionais_selecao(self) -> list:
        try:
            regionais = self.reginal_model.get_regional()
            
            dicionario_em_branco = {
                'id': None, 
                'nome': ''
            }
            
            if regionais:
                return [dicionario_em_branco] + regionais
            else:
                return [dicionario_em_branco]
            
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de patrimônio: {e}')