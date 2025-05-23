import streamlit as st
import datetime

from services.manutencoes_service import ManutencoesService

Manutencoes = ManutencoesService()

st.set_page_config(page_title='Relatórios de Manutenção', page_icon="favicon.ico", layout='wide')
st.title('📊 Relatórios de Manutenção')
st.markdown('---')


col1, col2 = st.columns(2)
data_inicio = col1.date_input(
    '📅 Início do Período',
    format='DD/MM/YYYY'
    )
data_fim = col2.date_input(
    '📅 Fim do Período',
    format='DD/MM/YYYY'
    )


iniciadas = Manutencoes.manutencoes_iniciadas(data_inicio, data_fim)
finalizadas = Manutencoes.manutencoes_finalizadas(data_inicio, data_fim)

col1, col2 = st.columns(2)
col1.metric('🔧 Manutenções em Aberto', len(iniciadas))
col2.metric('✅ Manutenções Finalizadas', len(finalizadas))
col1.dataframe(iniciadas)
col2.dataframe(finalizadas)

st.subheader('📅 Manutenções Realizadas no Período')
st.metric('Total de Manutenções do Periodo',len(iniciadas)+len(finalizadas))

st.subheader('🏢 Patrimônios na Oficina')
patrimonios_na_oficina = Manutencoes.listar_patrimonios_em_manutencao()
st.table(patrimonios_na_oficina)


# import plotly.express as px
# df_status = Manutencoes.contagem_por_status_df()
# fig = px.pie(df_status, names='status', values='total', title='Distribuição por Status')
# st.plotly_chart(fig, use_container_width=True)
