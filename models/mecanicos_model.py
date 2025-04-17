import streamlit as st

from core.database_manager import DatabaseManager

class MecanicosModel(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_mecanico(self) -> list:
        try:
            query = ''' SELECT 
                            mecanicos.id,
                            mecanicos.nome,
                            cargos.nome AS cargo,
                            regionais.nome AS regional
                        FROM mecanicos
                        JOIN cargos ON mecanicos.cargo_id = cargos.id
                        JOIN regionais ON mecanicos.regional_id = regionais.id;
                        '''
            mecanicos = self.fetch_all(query)
            if mecanicos:
                dados = [{'id':mecanico[0], 'nome':mecanico[1], 'cargo':mecanico[2], 'regional':mecanico[3]} for mecanico in mecanicos]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao recuperar informações de mecânico: {e}')
            return []

    def get_mecanico_by_id(self, id: int) -> dict:
        try:
            query = f'SELECT * FROM mecanico WHERE id = {id}'
            mecanico = self.fetch_one(query)
            if mecanico:
                return mecanico.fetchone()
            else:
                return None
        except Exception as e:
            st.error(f'Erro ao recuperar informações de mecânico: {e}')
            return None
        
    def _mecanico_existe(self, nome: str) -> bool:
        try:
            query = '''SELECT * FROM mecanicos WHERE nome = ?'''
            mecanico = self.fetch_one(query, (nome,))
            if mecanico:
                return True
            else:
                return False
        except Exception as e:
            st.error(f'Erro ao verificar mecânico: {e}')
            return True
    
    def create_mecanico(self, nome: str, cargo_id: int, regional_id: int) -> None:
        nome = nome.strip().upper()
        if self._mecanico_existe(nome):
            st.error("Mecânico já cadastrado.")
            return None
        try:
            query = f'INSERT INTO mecanicos (nome, cargo_id, regional_id) VALUES (?, ?, ?)'
            self.execute_query(query,(nome, cargo_id, regional_id))
        except Exception as e:
            st.error(f'Erro ao cadastrar mecânico: {e}')
        
    def get_cargos(self,) -> list:
        try:
            query = 'SELECT * FROM cargos'
            cargos = self.fetch_all(query)
            if cargos:
                dados = [{'id':cargo[0], 'nome':cargo[1]} for cargo in cargos]
                return dados
            else:
                return []
        except Exception as e:
            st.error(f'Erro ao recuperar informações de cargos: {e}')
            return []