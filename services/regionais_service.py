from models.regionais_model import RegionalModel

class RegionaisService:
    def __init__(self):
        self.reginal_model = RegionalModel()

    def listar_regionais(self) -> list:
        return self.reginal_model.get_regional()