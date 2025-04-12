import streamlit as st
from services.manutencoes_service import ManutencoesService
from services.patrimonios_service import PatrimoniosService
from services.mecanicos_service import MecanicosService

Manutencoes = ManutencoesService()
Patrimonios = PatrimoniosService()
Mecanicos = MecanicosService()

st.set_page_config(page_title="Entrada de Patrimônio", layout="wide")
st.title("📥 Registrar Entrada para Manutenção")

with st.form("entrada_form"):
    patrimonios = Patrimonios.listar_patrimonios()
    mecanicos = Mecanicos.listar_mecanicos()
    
    patrimonio = st.selectbox(
        "Patrimônio", 
        patrimonios, 
        format_func=lambda x: f"{x['numero']} - {x['modelo']}"
    )
    mecanico = st.selectbox(
        "Mecânico", 
        mecanicos, 
        format_func=lambda x: f"{x['nome']} ({x['cargo']})"
    )
    problema = st.text_area("Descrição do Problema")
    
    if st.form_submit_button("Registrar"):
        Manutencoes.registrar_entrada(patrimonio['id'], mecanico['id'], problema)
        st.success("Patrimônio registrado para manutenção!")