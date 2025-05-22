from models.locais_model import LocaisModel

class LocaisService:
    def __init__(self):
        self.local_model = LocaisModel()

    def listar_locais(self) -> list:
        locais = self.local_model.get_locais()
        if locais:
            return locais
        else:
            return []
        
    def _validar_dados_local(self, nome: str, regional_id: int) -> None:
        if not nome or len(nome.strip()) == 0:
            raise ValueError("O nome do local não pode ser vazio.")
        if regional_id is None:
            raise ValueError("A regional do local não pode ser vazia.")
        if self.local_model.local_ja_existe(nome):
            raise ValueError("Local já cadastrado.")
    
    def cadastrar_local(self, nome: str, regional_id: int) -> None:
        nome = nome.strip().upper()
        self._validar_dados_local(nome, regional_id)
        self.local_model.create_local(nome, regional_id)

    def excluir_localidade(self, local_id: int) -> None:
        self.local_model.delete_local(local_id)