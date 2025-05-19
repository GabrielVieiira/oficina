from models.mecanicos_model import MecanicosModel

class MecanicosService:
    def __init__(self):
        self.mecanico_model = MecanicosModel()

    def listar_mecanicos(self) -> list:
        return self.mecanico_model.get_mecanico() or []
    
    def mecanicos_selecao(self) -> list:
        try:
            mecanicos = self.mecanico_model.get_mecanico()
            
            dicionario_em_branco = {
                'id': None, 
                'nome': '',
                'cargo': '',
                'regional': ''
            }
            
            if mecanicos:
                return [dicionario_em_branco] + mecanicos
            else:
                return [dicionario_em_branco]
            
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de mecânicos: {e}')


    def buscar_mecanico(self, id: int) -> dict:
        return self.mecanico_model.get_mecanico_by_id(id)
    
    def _validar_dados_mecanico(self, nome: str, cargo_id: int, regional_id: int) -> None:
        if not nome or len(nome.strip()) == 0:
            raise ValueError("O nome do mecânico não pode ser vazio.")
        if cargo_id is None:
            raise ValueError("O cargo do mecânico não pode ser vazio.")
        if regional_id is None:
            raise ValueError("A regional do mecânico não pode ser vazia.")
        if self.mecanico_model.mecanico_ja_existe(nome):
            raise ValueError("Mecânico já cadastrado.")
           
    def cadastrar_mecanico(self, nome: str, cargo_id: int, regional_id: int) -> None:
        nome = nome.strip().upper()
        self._validar_dados_mecanico(nome, cargo_id, regional_id)
        self.mecanico_model.create_mecanico(nome, cargo_id, regional_id)

    def listar_cargos(self) -> list:
        return self.mecanico_model.get_cargos() or []
    
    def excluir_mecanico(self, id: int) -> None:
        self.mecanico_model.delete_mecanico(id)