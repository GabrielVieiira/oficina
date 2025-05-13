import streamlit as st
import utils
from services.manutencoes_service import ManutencoesService
from services.patrimonios_service import PatrimoniosService
from services.mecanicos_service import MecanicosService
from services.manutencao_classificacoes_service import ManutencaoClassificacoesService
from services.solicitantes_service import SolicitantesService
from services.regionais_service import RegionaisService
from services.manutencao_status_service import ManutencaoStatusService
from services.manutencao_status_service import ManutencaoStatusService

Manutencoes = ManutencoesService()
Patrimonios = PatrimoniosService()
Mecanicos = MecanicosService()
Classificacao = ManutencaoClassificacoesService()
Solicitantes = SolicitantesService()
Regionais = RegionaisService()
ManutencoesStatus = ManutencaoStatusService()
Status = ManutencaoStatusService()



st.title("🔧 Visualizar e Atualizar Manutenções")

st.markdown("### 🔍 Filtros de Busca")
col_f1, col_f2 = st.columns(2)

filtro_status = col_f1.selectbox(
    "Filtrar por status",
    ["Todos"] + [s['nome'] for s in Status.listar_manutencao_status()]
)

filtro_patrimonio = col_f2.selectbox(
        "🔍 Patrimônio", 
        Patrimonios.patrimonios_selecao(), 
        format_func=lambda x: f"{x['numeroPatrimonio']} - {x['modelo']}"
    )

manutencoes = Manutencoes.listar_manutencoes()

# Filtrar por status e número de patrimônio
if filtro_status != "Todos":
    manutencoes = [m for m in manutencoes if m['status_nome'] == filtro_status]
if filtro_patrimonio:
    manutencoes = [m for m in manutencoes if filtro_patrimonio['numero'] in m['numero_patrimonio']]

st.markdown("### 📋 Manutenções Registradas")
if not manutencoes:
    st.info("Nenhuma manutenção encontrada com os filtros selecionados.")
else:
    for manutencao in manutencoes:
        with st.expander(f"#{manutencao['numero_patrimonio']} | Entrada: {utils.formatar_data(manutencao['data_entrada'])} | Status: {manutencao['status_nome']}"):
            with st.form(f"form_atualizar_{manutencao['id']}", clear_on_submit=False):
                col1, col2 = st.columns(2)

                status_atual = col1.selectbox(
                    "Status",
                    Status.listar_manutencao_status(),
                    format_func=lambda x: x['nome'],
                    index=[s['nome'] for s in Status.listar_manutencao_status()].index(manutencao['status_nome'])
                )

                mecanico = col2.selectbox(
                    "Mecânico responsável",
                    Mecanicos.listar_mecanicos(),
                    format_func=lambda x: f"{x['nome']} ({x['cargo']})",
                    index=[m['nome'] for m in Mecanicos.listar_mecanicos()].index(manutencao['mecanico_nome'])
                )

                tipo_manutencao = col1.radio(
                    "Tipo de Manutenção",
                    ["CORRETIVA", "PREVENTIVA"],
                    index=["CORRETIVA", "PREVENTIVA"].index(manutencao['tipo_manutencao'])
                )

                tipo_mao_de_obra = col2.radio(
                    "Tipo de Mão de Obra",
                    ["PRÓPRIA", "TERCEIROS"],
                    index=["PRÓPRIA", "TERCEIROS"].index(manutencao['tipo_mao_de_obra'])
                )

                prioridade = col1.selectbox(
                    "Prioridade",
                    ["Baixa", "Média", "Alta"],
                    index=["Baixa", "Média", "Alta"].index(manutencao['prioridade'])
                )

                dt_inicio = col2.date_input("Data de Início", value=manutencao["inicio_manutencao"], format="DD/MM/YYYY")
                dt_previsao = col1.date_input("Previsão de Término", value=manutencao["previsao_termino"], format="DD/MM/YYYY")
                dt_termino = col2.date_input("Data de Término", value=manutencao["termino_manutencao"], format="DD/MM/YYYY")

                descricao = st.text_area("Descrição do Problema", value=manutencao['descricao'])

                if st.form_submit_button("💾 Salvar Atualizações"):
                    sucesso = Manutencoes.atualizar_manutencao(
                        id=manutencao['id'],
                        novo_status=status_atual['id'],
                        inicio_manutencao=dt_inicio,
                        tipo_mao_de_obra=tipo_mao_de_obra,
                        tipo_manutencao=tipo_manutencao,
                        nova_descricao=descricao,
                        data_entrada=manutencao['data_entrada'],
                        previsao_termino=dt_previsao,
                        novo_mecanico=mecanico['id'],
                        prioridade=prioridade,
                        data_termino_manutencao=dt_termino
                    )
                    if sucesso:
                        st.success("✅ Atualização salva com sucesso!")
                    else:
                        st.error("❌ Falha ao atualizar manutenção.")