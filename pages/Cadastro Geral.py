import streamlit as st

from services.mecanicos_service import MecanicosService
from services.regionais_service import RegionaisService
from services.centros_custo_service import CentroCustoService
from services.patrimonio_classificacoes_service import PatrimonioClassificacoesService
from services.patrimonios_service import PatrimoniosService
from services.solicitantes_service import SolicitantesService
from services.locais_service import LocaisService

Mecanicos = MecanicosService()
Regionais = RegionaisService()
CentroCusto = CentroCustoService()
Classificacao = PatrimonioClassificacoesService()
Patrimonios = PatrimoniosService()
Solicitantes = SolicitantesService()
Locais = LocaisService()

st.set_page_config(page_title='Cadastro', page_icon=':clipboard:', layout='wide')
st.title('📋 GERENCIAR')


aba_mecanicos, aba_patrimonios, aba_solicitantes, aba_locais, tab5 = st.tabs(['MECÂNICOS', 'PATRIMÔMIOS', 'SOLICITANTES', 'LOCAIS', 'PENDÊNCIAS'])
with aba_mecanicos:
    st.markdown('## 👨‍🔧 Cadastro de Mecânicos')
    st.markdown('---')
    
    with st.expander('➕ Novo Mecânico', expanded=True):
        with st.form('cadastro_mecanico', clear_on_submit=True):
            col1, col2 = st.columns(2)
            nome = col1.text_input('Nome completo')
            cargo = col2.selectbox('Cargo', Mecanicos.listar_cargos(), format_func=lambda x: x['nome'])
            regional = col1.selectbox('Regional', Regionais.listar_regionais(), format_func=lambda x: x['nome'])

            if st.form_submit_button('✅ Salvar'):
                try:
                    Mecanicos.cadastrar_mecanico(nome, cargo['id'], regional['id'])
                    st.success('✅ Mecânico cadastrado com sucesso!')
                except ValueError as ve:
                    st.warning(f'⚠️ Validação: {ve}')
                except Exception as e:
                    st.error(f'❌ Erro inesperado: {e}')

    with st.expander('👀 Visualizar Mecânicos'):
        mecanicos = Mecanicos.listar_mecanicos()
        if mecanicos:
            for m in mecanicos:
                with st.container():
                    col1, col2 = st.columns([5, 1])
                    col1.markdown(f'**Nome:** {m["nome"]}  |  **Cargo:** {m["cargo"]}  |  **Regional:** {m["regional"]}')
                    if col2.button('🗑️ Excluir', key=f'excluir_{m["id"]}'):
                        try:
                            Mecanicos.excluir_mecanico(m['id'])
                            st.success(f'Mecânico `{m["nome"]}` excluído com sucesso!')
                            st.rerun()
                        except Exception as e:
                            st.error(f'Erro ao excluir mecânico: {e}')
                st.divider()
        else:
            st.warning('Nenhum mecânico cadastrado.')
            
with aba_patrimonios:
    st.markdown('## 🚜 Cadastro de Patrimônios')
    st.markdown('---')

    with st.expander('➕ Novo Patrimônio', expanded=True):
        with st.form('cadastro_patrimonio', clear_on_submit=True):
            col1, col2 = st.columns(2)
            numero = col1.text_input('Número do Patrimônio')
            modelo = col2.text_input('Modelo')

            centro_de_custo = col1.selectbox('Centro de Custo', CentroCusto.listar_centros_custo(), format_func=lambda x: x['nome'])

            classificacao = col2.selectbox('Classificação', Classificacao.listar_patrimonio_classificacoes(), format_func=lambda x: x['nome'])
            proprio = col1.radio('Próprio?', ['Sim', 'Não'])

            if st.form_submit_button('✅ Salvar'):
                try:
                    Patrimonios.cadastrar_patrimonio(
                        numero,
                        centro_de_custo['id'],
                        modelo, classificacao['id'],
                        proprio == 'Sim'
                    )
                    st.success(f'✅ Patrimônio `{numero.upper()}` cadastrado com sucesso!')
                except ValueError as ve:
                    st.warning(f'⚠️ Validação: {ve}')
                except Exception as e:
                    st.error(f'❌ Erro inesperado: {e}')

    with st.expander('👀 Visualizar Patrimônios'):
        patrimonios = Patrimonios.listar_patrimonios()

        if patrimonios:
            for p in patrimonios:
                with st.container():
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.markdown(f'**#{p["numero_do_patrimonio"]}**')
                        st.markdown(f'🧾 Centro de Custo: {p["centroDeCusto"]} | Classificação: {p["classificacao"]}')
                        st.markdown(f'🚩 Próprio: {'✅ Sim' if p["proprio"] else '❌ Não'}')

                    with col2:
                            if st.button('🗑️ Excluir', key=f'excluir_patrimonio{p["id"]}'):
                                try:
                                    Patrimonios.excluir_patrimonio(p['id'])
                                    st.success(f'✅ Patrimônio `{p["numero_do_patrimonio"]}` excluído com sucesso!')
                                    st.rerun()
                                except Exception as e:
                                    st.error(f'❌ Erro ao excluir: {e}')
                st.divider()
        else:
            st.warning('Nenhum patrimônio cadastrado.')
            
with aba_solicitantes:
    st.markdown('## 🧍 Cadastro de Solicitantes')
    st.markdown('---')

    with st.expander('➕ Novo Solicitante', expanded=True):
        with st.form('cadastro_solicitante', clear_on_submit=True):
            nome = st.text_input('Nome completo')
            regional = st.selectbox('Regional', Regionais.listar_regionais(), format_func=lambda x: x['nome'])

            if st.form_submit_button('✅ Salvar'):
                try:
                    Solicitantes.cadastrar_solicitante(nome, regional['id'])
                    st.success('✅ Solicitante cadastrado!')
                except ValueError as ve:
                    st.warning(f'⚠️ Validação: {ve}')
                except Exception as e:
                    st.error(f'❌ Erro: {e}')

    with st.expander('👀 Visualizar Solicitantes'):
        solicitantes = Solicitantes.listar_solicitantes()
        if solicitantes:
            for s in solicitantes:
                with st.container():
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.markdown(f'**#{s["id"]}**')
                        st.markdown(f'🧾 Regional: {s["regional"]}')
                        st.markdown(f'📋 Nome: {s["nome"]}')

                    with col2:
                        if st.button('🗑️ Excluir', key=f'excluir_solicitante{s["id"]}'):
                            try:
                                Solicitantes.excluir_solicitante(s['id'])
                                st.success(f'✅ Solicitante `{s["nome"]}` excluído com sucesso!')
                                st.rerun()
                            except Exception as e:
                                st.error(f'❌ Erro ao excluir: {e}')
                st.markdown(f'**Nome:** {s["nome"]} | **Regional:** {s["regional"]}')
                st.divider()
        else:
            st.warning('Nenhum solicitante cadastrado.')

with aba_locais:
    st.markdown('## 🗺️ Cadastro de Locais')
    st.markdown('---')

    with st.form('cadastro_local', clear_on_submit=True):
        col1, col2 = st.columns(2)
        local = col1.text_input('Projeto/Local')
        regional = col2.selectbox('Regional', Regionais.listar_regionais(), format_func=lambda x: x['nome'])

        if st.form_submit_button('✅ Salvar'):
            try:
                Locais.cadastrar_local(local, regional['id'])
                st.success('✅ Local cadastrado com sucesso!')
            except ValueError as ve:
                st.warning(f'⚠️ Validação: {ve}')
            except Exception as e:
                st.error(f'❌ Erro ao cadastrar: {e}')

    with st.expander('👀 Visualizar Localidades'):
        localidades = Locais.listar_locais()
        if localidades:
            for l in localidades:
                with st.container():
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.markdown(f'**#{l["id"]}**')
                        st.markdown(f'🧾 Localiadde: {l["nome"]}')
                        st.markdown(f'📋 regional: {l["regional"]}')

                    with col2:
                        if st.button('🗑️ Excluir', key=f'excluir_localidade{l["id"]}'):
                            try:
                                Locais.excluir_localidade(l['id'])
                                st.success(f'✅ Localidade `{l["nome"]}` excluída com sucesso!')
                                st.rerun()
                            except Exception as e:
                                st.error(f'❌ Erro ao excluir: {e}')
                st.markdown(f'**Nome:** {l["nome"]} | **Regional:** {l["regional"]}')
                st.divider()
        else:
            st.warning('Nenhum solicitante cadastrado.')

with tab5:
    with st.form('Cadastro de pendência', clear_on_submit=True):
        regional = st.selectbox(
            'Regional', ['BRACELL', 'NEOMILLE', 'SUZANO', 'CERRADINHO', 'LACAN']
        )
        prioridade = st.selectbox('Prioridade', ['A', 'B', 'C'])
        data_deteccao = st.date_input('Data de detecção', format='DD/MM/YYYY')
        patrimonio = st.selectbox('Patrimônio', ['A', 'B', 'C', 'D'])
        comunicante = st.selectbox('Comunicante', ['A', 'B', 'C', 'D'])
        manutencao = st.selectbox(
            'Manutenção',
            [
                'BORRACHARIA',
                'ELÉTRICA',
                'MECÂNICA',
                'LIMPEZA/HIGIENIZAÇÃO',
                'SERRALHERIA/FUNILARIA/CONFECÇÃO',
                'SEGURANÇA',
            ],
        )
        tipo_manutencao = st.selectbox(
            'Tipo de manutenção',
            ['CORRETIVA', 'PREVENTIVA', 'PROGRAMADA', 'CONFECÇÃO', 'MELHORIA'],
        )
        if st.form_submit_button('Salvar'):
            st.success('Pendência cadastrada!!')
