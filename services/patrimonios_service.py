from models.patrimonios_model import PatrimoniosModel

class PatrimoniosService:
    def __init__(self):
        self.patrimonio_model = PatrimoniosModel()

    def listar_patrimonios(self) -> list:
        return self.patrimonio_model.get_patrimonio() or []
        
    # Método criado para retornar os dados do patrimônio em branco, para o selectbox do Streamlit    
    def patrimonios_selecao(self) -> list:
        try:
            patrimonios = self.patrimonio_model.get_patrimonio()
            
            dicionario_em_branco = {
                'id': None, 
                'numero_do_patrimonio': '', 
                'modelo': '',
                'proprio': None,
                'centroDeCusto': '', 
                'classificacao': ''
            }
            
            if patrimonios:
                return [dicionario_em_branco] + patrimonios
            else:
                return [dicionario_em_branco]
            
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de patrimônio: {e}')
        
    def _validar_dados_patrimonio(
        self, numero: str, centro_de_custo_id: int, modelo: str, classificacao_id: int
    ) -> None:
        if not numero or len(numero.strip()) == 0:
            raise ValueError("O número do patrimônio não pode ser vazio.")
        if centro_de_custo_id is None:
            raise ValueError("O centro de custo do patrimônio não pode ser vazio.")
        if not modelo or len(modelo.strip()) == 0:
            raise ValueError("O modelo do patrimônio não pode ser vazio.")
        if classificacao_id is None:
            raise ValueError("A classificação do patrimônio não pode ser vazia.")
        if self.patrimonio_model.patrimonio_ja_existe(numero):
            raise ValueError("Patrimônio já cadastrado.")
    
    def cadastrar_patrimonio(
        self, numero: str,
        centro_de_custo_id: int,
        modelo: str, classificacao_id: int,
        proprio: bool
        ) -> None:
        
        numero = numero.strip().upper()
        
        self._validar_dados_patrimonio(
            numero, centro_de_custo_id, modelo, classificacao_id
        )
        
        self.patrimonio_model.create_patrimonio(
            numero,
            centro_de_custo_id,
            modelo,
            classificacao_id,
            proprio
        )
        
    def excluir_patrimonio(self, patrimonio_id: int) -> None:        
        self.patrimonio_model.delete_patrimonio(patrimonio_id)