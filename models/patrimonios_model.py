import streamlit as st

from core.database_manager import DatabaseManager

class PatrimoniosModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_patrimonio(self) -> list:
        try:
            query = ''' SELECT 
                            patrimonios.id AS patrimonio_id,
                            patrimonios.numeroPatrimonio,
                            patrimonios.modelo,
                            patrimonios.ano,
                            patrimonios.placa,
                            patrimonios.proprio,
                            patrimonios.dataCadastro,
                            
                            centroDeCusto.nome AS centroDeCusto,
                            marca.nome AS marca,
                            combustivel.nome AS combustivel,
                            patrimonioClassificacao.nome AS classificacao

                        FROM patrimonios
                        JOIN centroDeCusto ON patrimonios.centroDeCusto_id = centroDeCusto.id
                        LEFT JOIN marca ON patrimonios.marca_id = marca.id
                        LEFT JOIN combustivel ON patrimonios.combustivel_id = combustivel.id
                        JOIN patrimonioClassificacao ON patrimonios.classificacao_id = patrimonioClassificacao.id
                        ORDER BY patrimonios.id; '''
            patrimonios = self.fetch_all(query)
            if patrimonios:
                dados = [{'id':patrimonio[0], 'numero':patrimonio[1], 'modelo':patrimonio[2], 'ano':patrimonio[3], 'placa':patrimonio[4], 'proprio':patrimonio[5], 'data_cadastro':patrimonio[6], 'centro_custo':patrimonio[7], 'marca':patrimonio[8], 'combustivel':patrimonio[9], 'classificacao':[10]} for patrimonio in patrimonios]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao recuperar informações de patrimônio: {e}')
            return []
        
    def get_patrimonio_by_id(self, id: int) -> dict:
        try:
            query = f'SELECT * FROM patrimonio WHERE id = {id}'
            patrimonio = self.fetch_one(query)
            if patrimonio:
                return patrimonio.fetchone()
            else:
                return None
        except Exception as e:
            st.error(f'Erro ao recuperar informações de patrimônio: {e}')
            return None
        
    def _verificar_patrimonio(self, numero: str) -> bool:
        try:
            query = f'SELECT * FROM patrimonios WHERE numeroPatrimonio = ?'
            patrimonio = self.fetch_one(query, (numero,))
            if patrimonio:
                return True
            else:
                return False
        except Exception as e:
            st.error(f'Erro ao verificar patrimônio: {e}')
            return False
        
    def _get_data_atual(self) -> str:
        try:
            query = 'SELECT datetime("now")'
            data = self.fetch_one(query)
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            st.error(f'Erro ao recuperar data atual: {e}')
            return None
    
    def create_patrimonio(
        self, numero: str, centro_de_custo_id: int, modelo: str, ano: int, placa: str, marca_id: int, combustivel_id: int, classificacao_id: int, proprio: bool
        ) -> None:
        numero = numero.strip().upper()
        existe = self._verificar_patrimonio(numero)
        if existe:
            st.error('Patrimônio já cadastrado!')
            return None
        try:
            query = f'INSERT INTO patrimonios (numeroPatrimonio, centroDeCusto_id, modelo, ano, placa, marca_id, combustivel_id, classificacao_id, proprio, dataCadastro) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            self.execute_query(query,(numero, centro_de_custo_id, modelo, ano, placa, marca_id, combustivel_id, classificacao_id, proprio, self._get_data_atual()))
        except Exception as e:
            st.error(f'Erro ao cadastrar patrimônio: {e}')