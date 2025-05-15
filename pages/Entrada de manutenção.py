import streamlit as st
from services.manutencoes_service import ManutencoesService
from services.patrimonios_service import PatrimoniosService
from services.mecanicos_service import MecanicosService
from services.manutencao_classificacoes_service import ManutencaoClassificacoesService
from services.solicitantes_service import SolicitantesService
from services.regionais_service import RegionaisService
from services.manutencao_status_service import ManutencaoStatusService
from services.tipo_manutencoes_service import TipoManutencaoService
from services.tipo_mao_de_obra_service import TipoMaoDeObraService
from services.locais_service import LocaisService


Manutencoes = ManutencoesService()
Patrimonios = PatrimoniosService()
Mecanicos = MecanicosService()
Classificacao = ManutencaoClassificacoesService()
Solicitantes = SolicitantesService()
Regionais = RegionaisService()
ManutencoesStatus = ManutencaoStatusService()
TipoManutencao = TipoManutencaoService()
TipoMaoDeObra = TipoMaoDeObraService()
Locais = LocaisService()

st.set_page_config(page_title="Entrada de Manutenção", layout="wide")

st.title("📥 Registrar Entrada para Manutenção")

st.markdown("---")

status_inicial = st.selectbox(
    "🚦 Status Inicial da Manutenção",
    ManutencoesStatus.status_permitidos_para_criacao(),
    format_func=lambda x: x['nome'],
    key="manutencao_iniciada_select"
)

with st.form("entrada_form"):
    col1, col2, col3 = st.columns(3)

    patrimonio = col1.selectbox(
        "🔍 Patrimônio",
        Patrimonios.patrimonios_selecao(),
        format_func=lambda x: f"{x['numeroPatrimonio']} - {x['modelo']}"
    )

    regional = col2.selectbox(
        "🏢 Regional",
        Regionais.regionais_selecao(),
        format_func=lambda x: x['nome']
    )

    solicitante = col3.selectbox(
        "🙋 Solicitante",
        Solicitantes.solicitantes_selecao(),
        format_func=lambda x: x['nome']
    )

    col4, col5, col6 = st.columns(3)
    classificacao_manutencao = col4.selectbox(
        "📋 Classificação",
        Classificacao.manutencao_classificacoes_selecao(),
        format_func=lambda x: x['nome']
    )

    prioridade = col5.selectbox(
        "⚠️ Prioridade",
        ["", "Baixa", "Média", "Alta"]
    )

    locais = col6.selectbox(
        "📍 Local de Execução",
        Locais.listar_locais(),
        format_func=lambda x: x['nome']
    )

    col7, col8 = st.columns(2)
    data_entrada = col7.date_input("📅 Data de Entrada", format="DD/MM/YYYY")
    tipo_manutencao = st.radio(
        "🛠 Tipo de Manutenção",
        TipoManutencao.listar_tipos_manutencao(),
        format_func=lambda x: x['nome'],
        horizontal=True
        )

    col9, col10 = st.columns(2)
    qtd_horas_mecanico = col9.number_input("⏱️ Horas Previstas de Mecânico", format="%d", step=1)
    tipo_mao_obra = col10.radio("🧑‍🏭 Tipo de Mão de Obra", TipoMaoDeObra.listar_tipos_mao_de_obra(), format_func=lambda x: x['nome'], horizontal=True)
    mecanico = None
    data_inicio = None
    data_termino = None
    resolucao_problema = ""

    if status_inicial['nome'] in ["INICIADO", "FINALIZADO"]:
        mecanico = col9.selectbox("👨‍🔧 Mecânico Responsável", Mecanicos.listar_mecanicos(), format_func=lambda x: f"{x['nome']} ({x['cargo']})")
        data_inicio = col9.date_input("📆 Início da Manutenção", format="DD/MM/YYYY")

    if status_inicial['nome'] == "FINALIZADO":
        data_termino = col9.date_input("🏁 Término da Manutenção", format="DD/MM/YYYY")
        resolucao_problema = st.text_area("🔧 Resolução do Problema", height=80)

    descricao_problema = st.text_area("📄 Descrição do Problema Encontrado", height=100)
    observacao = st.text_area("🗒️ Observações", height=80)

    if st.form_submit_button("✅ Registrar"):
        try:
            Manutencoes.cadastrar_manutencao(
                status_id=status_inicial['id'],
                patrimonio_id=patrimonio['id'],
                regional_id=regional['id'],
                solicitante_id=solicitante['id'],
                manutencao_classificacao_id=classificacao_manutencao['id'],
                prioridade=prioridade,
                tipo_manutencao_id=tipo_manutencao['id'],
                dt_entrada=data_entrada,
                problema_descricao=descricao_problema,
                observacao=observacao,
                mecanico_id=mecanico['id'] if mecanico else None,
                dt_inicio_manutencao=data_inicio,
                dt_termino_manutencao=data_termino,
                tipo_mao_de_obra_id=tipo_mao_obra['id'] if tipo_mao_obra else None,
                qtd_horas_mecanico=qtd_horas_mecanico,
                resolucao_do_problema=resolucao_problema,
                locais_id=locais['id']
            )
            st.success(f"🔧 Manutenção para o patrimônio `{patrimonio['numeroPatrimonio']}` registrada com sucesso!")
        except ValueError as ve:
            st.error(f"❌ Erro de validação: {ve}")
        except Exception as e:
            st.error(f"⚠️ Erro ao registrar: {e}")