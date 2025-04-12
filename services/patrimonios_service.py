from models.patrimonios_model import PatrimoniosModel

class PatrimoniosService:
    def __init__(self):
        self.patrimonio_model = PatrimoniosModel()

    def listar_patrimonios(self) -> list:
        try:
            patrimonios = self.patrimonio_model.get_patrimonio()
            if patrimonios:
                return patrimonios
            else:
                return []
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de patrimônio: {e}')
        
    def cadastrar_patrimonio(
        self, numero: str, centro_de_custo_id: int, modelo: str, ano: int, placa: str, marca_id: int, combustivel_id: int, classificacao_id: int, proprio: bool
        ) -> None:
        try:
            self.patrimonio_model.create_patrimonio(
                numero,
                centro_de_custo_id,
                modelo,
                ano,
                placa,
                marca_id,
                combustivel_id,
                classificacao_id,
                proprio
            )
        except Exception as e:
            raise Exception(f'Erro ao cadastrar patrimônio: {e}')