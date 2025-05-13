from models.solicitante_model import SolicitantesModel


class SolicitantesService:
    def __init__(self):
        self.solicitantes_model = SolicitantesModel()

    def _validar_dados_solicitante(self, nome: str, regional: int) -> None:
        if not nome or len(nome.strip()) == 0:
            raise ValueError("O nome do solicitante não pode ser vazio.")
        if regional is None:
            raise ValueError("A regional do solicitante não pode ser vazia.")
        if self.solicitantes_model.solicitante_ja_existe(nome):
            raise ValueError("Solicitante já cadastrado.")
    
    def cadastrar_solicitante(self, nome: str, regional: int) -> None:
        nome = nome.strip().upper()
        self._validar_dados_solicitante(nome, regional)
        self.solicitantes_model.create_solicitante(nome, regional)

    def listar_solicitantes(self) -> list:
        return self.solicitantes_model.get_solicitantes()
    
    def solicitantes_selecao(self) -> list:
        try:
            solicitantes = self.solicitantes_model.get_solicitantes()
            dicionario_em_branco = {
                'id': None, 
                'nome': '',
                'regional': ''
            }
            if solicitantes:
                return [dicionario_em_branco] + solicitantes
            else:
                return [dicionario_em_branco]
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de solicitantes: {e}')