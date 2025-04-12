import streamlit as st

from services.mecanicos_service import MecanicosService
from services.regionais_service import RegionaisService
from services.centros_custo_service import CentroCustoService
from services.marcas_service import MarcasService
from services.combustiveis_service import CombustiveisService
from services.patrimonio_classificacoes_service import PatrimonioClassificacoesService
from services.patrimonios_service import PatrimoniosService
from services.solicitantes_service import SolicitantesService

Mecanicos = MecanicosService()
Regionais = RegionaisService()
CentroCusto = CentroCustoService()
Marcas = MarcasService()
Combustivel = CombustiveisService()
Classificacao = PatrimonioClassificacoesService()
Patrimonios = PatrimoniosService()
Solicitantes = SolicitantesService()

st.set_page_config(page_title="Cadastro", page_icon=":clipboard:", layout="wide")

tipos_de_cadastro = ["MECÂNICO", "PATRIMÔMIO","SOLICITANTE", "LOCAL", "PENDÊNCIA"]
tipo = st.sidebar.selectbox("Escolha o que deseja cadastrar", tipos_de_cadastro)


def validar_form(*campos):
    return all(campos)

if tipo == "MECÂNICO":
    with st.expander('Cadatrar Mecânico', expanded=True):
        with st.form("Cadastro de executante", clear_on_submit=True):
            nome = st.text_input("Nome")
            cargo = st.selectbox(
                'Cargo', Mecanicos.listar_cargos(), format_func=lambda x: x['nome']
                )
            regional = st.selectbox(
                "Regional", Regionais.listar_regionais(), format_func=lambda x: x['nome']
            )
            if st.form_submit_button("Salvar"):
                if nome:
                    Mecanicos.cadastrar_funcionario(nome, cargo['id'], regional['id'])
                    st.success("Executante cadastrado!!")
                else:
                    st.error("Preencha todos os campos!!")
                    
    with st.expander('Visualizar Mecânicos'):
        mecanicos = Mecanicos.listar_mecanicos()
        if mecanicos:
            for mecanico in mecanicos:
                st.write(f"Nome: {mecanico['nome']}")
                st.write(f"Cargo: {mecanico['cargo']}")
                st.write(f"Regional: {mecanico['regional']}")
                st.write("---")
        else:
            st.warning("Nenhum mecânico cadastrado.")
            
elif tipo == "PATRIMÔMIO":
    with st.expander('Cadatrar Patrimônio', expanded=True):
        with st.form("Cadastro de Patrimônio", clear_on_submit=True):
            patrimonio = st.text_input("Número do patrimônio")
            centro_de_custo = st.selectbox(
                "Centro de custo", CentroCusto.listar_centros_custo(), format_func=lambda x: x['nome']
            )
            modelo = st.text_input("Modelo")
            ano = st.number_input(
                "Ano", format="%0.0f"
                )
            placa = st.text_input("Placa")
            marca = st.selectbox(
                "Marca", Marcas.listar_marcas(), format_func=lambda x: x['nome']
            )
            combustivel = st.selectbox(
                "Combustível", Combustivel.listar_combustiveis(), format_func=lambda x: x['nome']
            )
            classificacao = st.selectbox(
                "Classificação", Classificacao.listar_classificacoes(), format_func=lambda x: x['nome']
            )
            proprio = st.radio("Próprio?", options=["Sim", "Não"])
            if st.form_submit_button("Salvar"):
                if validar_form(
                    patrimonio,
                    centro_de_custo,
                    modelo,
                    ano,
                    placa,
                    marca,
                    combustivel,
                    proprio,
                ):
                    Patrimonios.cadastrar_patrimonio(
                        patrimonio,
                        centro_de_custo['id'],
                        modelo,
                        ano,
                        placa,
                        marca['id'],
                        combustivel['id'],
                        classificacao['id'],
                        proprio == "Sim",
                    )
                else:
                    st.error("Preencha todos os campos!!")

    with st.expander('Visualizar Patrimônios'):
        patrimonios = Patrimonios.listar_patrimonios()
        if patrimonios:
            for patrimonio in patrimonios:
                st.write(f"Patrimônio: {patrimonio['numero']}")
                st.write(f"Centro de Custo: {patrimonio['centro_custo']}")
                st.write(f"Modelo: {patrimonio['modelo']}")
                st.write(f"Ano: {patrimonio['ano']}")
                st.write(f"Placa: {patrimonio['placa']}")
                st.write(f"Marca: {patrimonio['marca']}")
                st.write(f"Combustível: {patrimonio['combustivel']}")
                st.write(f"Próprio: {patrimonio['proprio']}")
                st.write("---")
        else:
            st.warning("Nenhum patrimônio cadastrado.")
            
elif tipo == "SOLICITANTE":
    with st.expander('Cadatrar Solicitante', expanded=True):
        with st.form("Cadastro de solicitante", clear_on_submit=True):
            nome = st.text_input("Nome")
            cargo = st.selectbox(
                "Cargo", Mecanicos.listar_cargos(), format_func=lambda x: x['nome']
            )
            regional = st.selectbox(
                "Regional", Regionais.listar_regionais(), format_func=lambda x: x['nome']
            )
            if st.form_submit_button("Salvar"):
                if nome:
                    Solicitantes.cadastrar_solicitante(nome, cargo['id'], regional['id'])
                    st.success("Solicitante cadastrado!!")
                else:
                    st.error("Preencha todos os campos!!")

    with st.expander('Visualizar Solicitantes'):
        solicitantes = Solicitantes.listar_solicitantes()
        if solicitantes:
            for solicitante in solicitantes:
                st.write(f"Nome: {solicitante['nome']}")
                st.write(f"Cargo: {solicitante['cargo']}")
                st.write(f"Regional: {solicitante['regional']}")
                st.write("---")
        else:
            st.warning("Nenhum solicitante cadastrado.")

elif tipo == "LOCAL":
    with st.form("Cadastro de local", clear_on_submit=True):
        local = st.text_input("Projeto/Local")
        municipio = st.text_input("Município")
        regional = st.text_input("Regional")
        if st.form_submit_button("Salvar"):
            if validar_form(local, municipio, regional):
                st.success("Local cadastrado!!")
            else:
                st.error("Preencha todos os campos!!")

elif tipo == "PENDÊNCIA":
    with st.form("Cadastro de pendência", clear_on_submit=True):
        regional = st.selectbox(
            "Regional", ["BRACELL", "NEOMILLE", "SUZANO", "CERRADINHO", "LACAN"]
        )
        prioridade = st.selectbox("Prioridade", ["A", "B", "C"])
        data_deteccao = st.date_input("Data de detecção", format="DD/MM/YYYY")
        patrimonio = st.selectbox("Patrimônio", ["A", "B", "C", "D"])
        comunicante = st.selectbox("Comunicante", ["A", "B", "C", "D"])
        manutencao = st.selectbox(
            "Manutenção",
            [
                "BORRACHARIA",
                "ELÉTRICA",
                "MECÂNICA",
                "LIMPEZA/HIGIENIZAÇÃO",
                "SERRALHERIA/FUNILARIA/CONFECÇÃO",
                "SEGURANÇA",
            ],
        )
        tipo_manutencao = st.selectbox(
            "Tipo de manutenção",
            ["CORRETIVA", "PREVENTIVA", "PROGRAMADA", "CONFECÇÃO", "MELHORIA"],
        )
        if st.form_submit_button("Salvar"):
            if validar_form(
                regional,
                prioridade,
                data_deteccao,
                patrimonio,
                comunicante,
                manutencao,
                tipo_manutencao,
            ):
                st.success("Pendência cadastrada!!")
            else:
                st.error("Preencha todos os campos!!")
