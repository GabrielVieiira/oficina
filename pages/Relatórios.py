import streamlit as st
from services.manutencoes_service import ManutencoesService
from services.patrimonios_service import PatrimoniosService

Patrimonios = PatrimoniosService()
Manutencoes = ManutencoesService()

st.set_page_config(page_title='Relatórios de Manutenção', page_icon="./favicon.ico", layout='wide')
st.title('📊 Relatórios de Manutenção')
st.markdown('---')

# Tabs
aba_relatorios, aba_oficina = st.tabs(["📈 Resumo do Período", "🏢 Na Oficina"])

with aba_relatorios:
    st.subheader('📅 Manutenções Realizadas no Período')
    col1, col2 = st.columns(2)
    data_inicio = col1.date_input('📅 Início do Período', format='DD/MM/YYYY')
    data_fim = col2.date_input('📅 Fim do Período', format='DD/MM/YYYY')

    iniciadas = Manutencoes.manutencoes_iniciadas(data_inicio, data_fim)
    finalizadas = Manutencoes.manutencoes_finalizadas(data_inicio, data_fim)

    st.metric('Total de Manutenções do Período', len(iniciadas) + len(finalizadas))
    
    col1, col2 = st.columns(2)
    col1.metric('🔧 Manutenções em Aberto', len(iniciadas))
    col2.metric('✅ Manutenções Finalizadas', len(finalizadas))

    col1.dataframe(iniciadas, use_container_width=True, hide_index=True)
    col2.dataframe(finalizadas, use_container_width=True, hide_index=True)



with aba_oficina:
    st.subheader("🏢 Patrimônios atualmente na Oficina")
    patrimonios_na_oficina = Manutencoes.listar_patrimonios_na_oficina()

    if not patrimonios_na_oficina:
        st.info("Nenhum patrimônio se encontra na oficina no momento.")
    else:
        for p in patrimonios_na_oficina:
            with st.expander(f"🔧 {p['numero_do_patrimonio']} | Entrada: {p['dt_entrada']}"):
                col1, col2 = st.columns(2)
                col1.markdown(f"**Modelo:** `{p['modelo']}`")
                col2.markdown(f"**Status Atual:** `{p['status']}`")

                st.markdown(f"**Data de Entrada:** `{p['dt_entrada']}`")

                with st.form(f"form_saida_{p['manutencao_id']}"):
                    data_saida = st.date_input(
                        "📅 Data de Saída",
                        format="DD/MM/YYYY",
                        key=f"data_saida_{p['manutencao_id']}"
                    )
                    confirmar = st.form_submit_button("✅ Confirmar Saída")

                    if confirmar:
                        try:
                            Manutencoes.registrar_saida_da_oficina(p['manutencao_id'], data_saida)
                            st.success("🚗 Saída registrada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao registrar saída: {e}")