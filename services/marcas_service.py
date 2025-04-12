from models.marcas_model import MarcaModel


class MarcasService:
    def __init__(self):
        self.marca_model = MarcaModel()

    def listar_marcas(self) -> list:
        try:
            marcas = self.marca_model.get_marcas()
            if marcas:
                return marcas
            else:
                return []
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de marcas: {e}')