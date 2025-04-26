import streamlit as st
import utils
from services.manutencoes_service import ManutencoesService
from services.patrimonios_service import PatrimoniosService
from services.mecanicos_service import MecanicosService
from services.manutencao_classificacoes_service import ManutencaoClassificacoesService
from services.solicitantes_service import SolicitantesService
from services.regionais_service import RegionaisService
from services.manutencao_status_service import ManutencaoStatusService

Manutencoes = ManutencoesService()
Patrimonios = PatrimoniosService()
Mecanicos = MecanicosService()
Classificacao = ManutencaoClassificacoesService()
Solicitantes = SolicitantesService()
Regionais = RegionaisService()
ManutencoesStatus = ManutencaoStatusService()

st.set_page_config(page_title="Entrada de Manutenção", layout="wide")

st.title("📥 Registrar Entrada para Manutenção")

tab1, tab2, tab3 = st.tabs(["Entrada de patrimônio", "Atualizar manutenção", "Saída de patrimônio"])
with tab1:
    with st.form("entrada_form"):
        col1, col2 = st.columns(2)
        
        patrimonio = col1.selectbox(
            "Patrimônio", 
            Patrimonios.patrimonios_selecao(), 
            format_func=lambda x: f"{x['numero']} - {x['modelo']}"
        )
        
        regional = col2.selectbox(
            "Regional", 
            Regionais.regionais_selecao(), 
            format_func=lambda x: f"{x['nome']}"
        )
        
        # mecanico = col1.selectbox(
        #     "Mecânico responsável", 
        #     Mecanicos.mecanicos_selecao(), 
        #     format_func=lambda x: f"{x['nome']} ({x['cargo']})"
        # )
        
        solicitante = col2.selectbox(
            "Solicitante", 
            Solicitantes.solicitantes_selecao(), 
            format_func=lambda x: f"{x['nome']}"
        )
        
        classificacao_manutencao = col1.selectbox(
            "Classificação de Manutenção", 
            Classificacao.manutencao_classificacoes_selecao(), 
            format_func=lambda x: x['nome']
        )
        
        prioridade = col2.selectbox(
            "Prioridade", 
            ["","Baixa", "Média", "Alta"],
            format_func=lambda x: x
        )
        
        data_entrada = col1.date_input(
            "Data de Entrada",
            format="DD/MM/YYYY",
            value=None
            )
        
        tipo_manutencao = col1.radio(
            "Tipo de Manutenção",
            ["CORRETIVA", "PREVENTIVA"]
            )
           
        # tipo_mao_de_obra = col2.radio(
        #     'Mão de obra', 
        #     ['PRÓPRIA', 'TERCEIROS']
        #     )
        
        # previsao_termino = col2.date_input(
        #     "Previsão de termino da manutenção",
        #     format="DD/MM/YYYY",
        #     value=None
        #     )
        
        descricao_problema = st.text_area("Descrição do Problema")
        observacao = st.text_area("Observação") 
        
        # qtd_horas_previstas = col1.number_input(
        #         "Quantidade de horas previstas", format="%0.0f"
        #         )
        
        
        
        # valor_hora_mecanico = col2.number_input(
        #         "Valor da hora do mecânico", format="%0.2f"
        #         )
                
        if st.form_submit_button("Registrar"):
            try:
                sucesso_cadastro =  Manutencoes.registrar_entrada(
                    patrimonio['id'],
                    regional['id'],
                    solicitante['id'],
                    classificacao_manutencao['id'],
                    prioridade,
                    tipo_manutencao,
                    data_entrada,
                    descricao_problema,
                    observacao,
                    )
                st.success("Patrimônio registrado para manutenção!")
            except ValueError as ve:
                st.error(f"Erro de validação: {ve}")
            except Exception as e:
                st.error(f"Erro ao registrar entrada de manutenção: {e}")
with tab2:
    opcoes_filtro = ["Todas", "Aguardando planejamento", "Iniciadas", "Aguardando peças", "Canceladas", "Finalizadas"]   
    st.subheader("🔧 Atualizar Manutenção Existente")

    filtro = st.sidebar.selectbox("Selecione o status da manutenção", opcoes_filtro, index=0)
    periodo_de = st.sidebar.date_input("Selecione o período", value=None, format="DD/MM/YYYY", key="periodo_de")
    periodo_ate = st.sidebar.date_input("Selecione o período", value=None, format="DD/MM/YYYY", key="periodo_ate") 
    st.sidebar.markdown("**Observação:** O período é considerado apenas para as manutenções que estão em andamento ou concluídas.")

    manutencoes = Manutencoes.listar_manutencoes()
    if not manutencoes:
        st.info("Nenhuma manutenção disponível para atualizar.")
    else:
        manutencao = st.selectbox(
            "Selecione uma manutenção para atualizar",
            manutencoes,
            format_func=lambda x: f"# {x['numero_patrimonio']} | Data de entrada: {utils.formatar_data(x['data_entrada'])} | Status: {x['status_nome']}"
        )

        with st.form("form_atualizacao"):
            col1, col2 = st.columns(2)

            novo_status = col1.selectbox(
                "Status",
                ManutencoesStatus.listar_manutencao_status(),
                format_func=lambda x: x['nome'],
                index=[status['nome'] for status in ManutencoesStatus.listar_manutencao_status()].index(manutencao['status_nome']),
                )
            
            inicio_manutencao = col2.date_input(
                "Data de início da manutenção",
                value=manutencao["inicio_manutencao"],
                format="DD/MM/YYYY"
            )
            
            novo_mecanico = col2.selectbox(
                "Mecânico responsável",
                Mecanicos.listar_mecanicos(),
                format_func=lambda x: f"{x['nome']} ({x['cargo']})",
                index=[mecanico['nome'] for mecanico in Mecanicos.listar_mecanicos()].index(manutencao['mecanico_nome'])
            )
            
            nova_prioridade = col1.selectbox(
                "Prioridade",
                ["Baixa", "Média", "Alta"],
                index=["Baixa", "Média", "Alta"].index(manutencao['prioridade'])
            )

            data_entrada = col1.date_input(
                "Data de entrada",
                value=manutencao["data_entrada"],
                format="DD/MM/YYYY"
            )

            data_termino_manutencao = col1.date_input(
                "Data de termino da manutenção",
                value=manutencao["termino_manutencao"],
                format="DD/MM/YYYY"
            )
            
            previsao_termino = col2.date_input(
                "Previsão de término",
                value=manutencao["previsao_termino"],
                format="DD/MM/YYYY"
            )
            
            novo_tipo_mao_de_obra = col1.radio("Tipo de mão de obra", ["PRÓPRIA", "TERCEIROS"], index=["PRÓPRIA", "TERCEIROS"].index(manutencao["tipo_mao_de_obra"]))

            novo_tipo_manutencao = col2.radio(
                "Tipo de Manutenção",
                ["CORRETIVA", "PREVENTIVA"],
                index=["CORRETIVA", "PREVENTIVA"].index(manutencao['tipo_manutencao'])
            )
            nova_descricao = st.text_area("Atualizar descrição do problema", value=manutencao["descricao"])
            if st.form_submit_button("Salvar Alterações"):
                sucesso = Manutencoes.atualizar_manutencao(
                    id=manutencao["id"],
                    novo_status=novo_status['id'],
                    inicio_manutencao=inicio_manutencao,
                    tipo_mao_de_obra=novo_tipo_mao_de_obra,
                    tipo_manutencao=novo_tipo_manutencao,
                    nova_descricao=nova_descricao,
                    data_entrada=data_entrada,
                    previsao_termino=previsao_termino,
                    novo_mecanico=novo_mecanico['id'],
                    prioridade=nova_prioridade,
                    data_termino_manutencao=data_termino_manutencao
                )
                if sucesso:
                    st.success("Manutenção atualizada com sucesso!")
                else:
                    st.error("Erro ao atualizar manutenção.")
                    
with tab3:
    manutencao_saida = st.selectbox(
        "Selecione uma manutenção para registrar saída",
        Manutencoes.listar_concluidos(),
        format_func=lambda x: f"#{x['numero_patrimonio']} | Status: {x['status_nome']}"
    )
    with st.form("form_saida"):
        col1, col2 = st.columns(2)
        patrimonio_saida = col1.selectbox(
            "Patrimônio",
            manutencao_saida['numero_patrimonio'],
            disabled=True
            )

        data_saida = col2.date_input(
            "Data de saída",
            value=manutencao_saida['termino_manutencao'],
            format="DD/MM/YYYY"
        )

        if st.form_submit_button("Registrar Saída"):
            ...