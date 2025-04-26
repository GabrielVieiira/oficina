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
        
    # Método criado para retornar os dados do patrimônio em branco, para o selectbox do Streamlit    
    def patrimonios_selecao(self) -> list:
        try:
            patrimonios = self.patrimonio_model.get_patrimonio()
            
            dicionario_em_branco = {
                'id': None, 
                'numero': '', 
                'modelo': '', 
                'ano': None, 
                'placa': '', 
                'proprio': None, 
                'data_cadastro': None, 
                'centro_custo': '', 
                'marca': '', 
                'combustivel': '', 
                'classificacao': ''
            }
            
            if patrimonios:
                return [dicionario_em_branco] + patrimonios
            else:
                return [dicionario_em_branco]
            
        except Exception as e:
            raise Exception(f'Erro ao recuperar informações de patrimônio: {e}')
        
    def _validar_dados_patrimonio(
        self, numero: str, centro_de_custo_id: int, modelo: str, ano: int, placa: str, marca_id: int, combustivel_id: int, classificacao_id: int, proprio: bool
    ) -> None:
        if not numero or len(numero.strip()) == 0:
            raise ValueError("O número do patrimônio não pode ser vazio.")
        if centro_de_custo_id is None:
            raise ValueError("O centro de custo do patrimônio não pode ser vazio.")
        if not modelo or len(modelo.strip()) == 0:
            raise ValueError("O modelo do patrimônio não pode ser vazio.")
        if ano is None or ano <1900 or ano > 2025:
            raise ValueError("O ano do patrimônio não pode ser vazio.")
        if not placa or len(placa.strip()) == 0:
            raise ValueError("A placa do patrimônio não pode ser vazia.")
        if marca_id is None:
            raise ValueError("A marca do patrimônio não pode ser vazia.")
        if combustivel_id is None:
            raise ValueError("O combustível do patrimônio não pode ser vazio.")
        if classificacao_id is None:
            raise ValueError("A classificação do patrimônio não pode ser vazia.")
        if self.patrimonio_model.patrimonio_ja_existe(numero):
            raise ValueError("Patrimônio já cadastrado.")
    
    def cadastrar_patrimonio(
        self, numero: str, centro_de_custo_id: int, modelo: str, ano: int, placa: str, marca_id: int, combustivel_id: int, classificacao_id: int, proprio: bool
        ) -> None:
        numero = numero.strip().upper()
        try:
            self._validar_dados_patrimonio(
                numero, centro_de_custo_id, modelo, ano, placa, marca_id, combustivel_id, classificacao_id, proprio
            )
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
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f'Erro ao cadastrar patrimônio: {e}')