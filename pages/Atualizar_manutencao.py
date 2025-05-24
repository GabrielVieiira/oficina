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
from services.prioridades_service import PrioridadesService


Manutencoes = ManutencoesService()
Patrimonios = PatrimoniosService()
Mecanicos = MecanicosService()
ClassificacaoManutencao = ManutencaoClassificacoesService()
Solicitantes = SolicitantesService()
Regionais = RegionaisService()
ManutencoesStatus = ManutencaoStatusService()
TipoManutencao = TipoManutencaoService()
TipoMaoDeObra = TipoMaoDeObraService()
Locais = LocaisService()
Prioridades = PrioridadesService()

st.set_page_config(page_title='Atualizar Manutenção', page_icon="./favicon.ico", layout='wide')

st.title('🔧 Atualizar Manutenções')

st.markdown('### 🔍 Filtros')
col1, col2 = st.columns(2)

filtro_status = col1.selectbox(
    'Filtrar por Status',
    ['Todos'] + [s['nome'] for s in ManutencoesStatus.listar_manutencao_status()]
)

filtro_patrimonio = col2.selectbox(
    'Filtrar por Patrimônio',
    Patrimonios.patrimonios_selecao(),
    format_func=lambda x: f'{x["numero_do_patrimonio"]} - {x["modelo"]}'
)


manutencoes = Manutencoes.listar_manutencoes()
mecanicos = Mecanicos.listar_mecanicos()
status_list = ManutencoesStatus.listar_manutencao_status()

if manutencoes:

    if filtro_status != 'Todos':
        status_id = next((s['id'] for s in status_list if s['nome'] == filtro_status), None)
        manutencoes = [m for m in manutencoes if m['status_de_manutencao_id'] == status_id]

    if filtro_patrimonio['id']:
        manutencoes = [m for m in manutencoes if m['patrimonio_id'] == filtro_patrimonio['id']]

    for manutencao in manutencoes:
        with st.expander(f'Manutenção #{manutencao["id"]}'):
            col1, col2, col3 = st.columns(3)

            patrimonio = col1.selectbox(
                '🔍 Patrimônio',
                Patrimonios.listar_patrimonios(),
                format_func=lambda x: f'{x["numero_do_patrimonio"]} - {x["modelo"]}',
                index=[p['id'] for p in Patrimonios.listar_patrimonios()].index(manutencao['patrimonio_id']) if manutencao['patrimonio_id'] else 0,
                key=f'patrimonio_{manutencao["id"]}',
                disabled=True
            )

            regional = col2.selectbox(
                '🏢 Regional',
                Regionais.listar_regionais(),
                format_func=lambda x: x['nome'],
                index=[r['id'] for r in Regionais.listar_regionais()].index(manutencao['regional_id']) if manutencao['regional_id'] else 0,
                key=f'regional_{manutencao["id"]}',
                disabled=True
            )

            solicitante = col3.selectbox(
                '🙋 Solicitante',
                Solicitantes.listar_solicitantes(),
                format_func=lambda x: x['nome'],
                index=[s['id'] for s in Solicitantes.listar_solicitantes()].index(manutencao['solicitante_id']) if manutencao['solicitante_id'] else 0,
                key=f'solicitante_{manutencao["id"]}',
            )

            col4, col5, col6 = st.columns(3)
            manutencao_classificacao = col4.selectbox(
                '📋 Classificação',
                ClassificacaoManutencao.listar_manutencao_classificacoes(),
                format_func=lambda x: x['nome'],
                index=[c['id'] for c in ClassificacaoManutencao.listar_manutencao_classificacoes()].index(manutencao['classificacao_de_manutencao_id']) if manutencao['patrimonio_id'] else 0,
                key=f'classificacao_{manutencao["id"]}'
            )

            prioridade = col5.selectbox(
                '⚠️ Prioridade',
                Prioridades.listar_prioridades(),
                format_func=lambda x: x['nome'],
                index=[p['id'] for p in Prioridades.listar_prioridades()].index(manutencao['prioridade_id']) if manutencao['prioridade_id'] else 0,
                key=f'prioridade_{manutencao["id"]}'
            )

            locais = col6.selectbox(
                '📍 Local de Execução',
                Locais.listar_locais(),
                format_func=lambda x: x['nome'],
                index=[l['id'] for l in Locais.listar_locais()].index(manutencao['localidade_id']) if manutencao['localidade_id'] else 0,
                key=f'local_{manutencao["id"]}'
            )

            col7, col8 = st.columns(2)
            data_entrada = col7.date_input(
                '📅 Data de Entrada',
                format='DD/MM/YYYY',
                value=manutencao['dt_entrada'],
                key=f'data_entrada_{manutencao["id"]}',
                )

            status_manutencao = col8.selectbox(
                '🚦 Status da Manutenção',
                status_list,
                format_func=lambda x: x['nome'],
                index=[s['id'] for s in status_list].index(manutencao['status_de_manutencao_id']),
                key=f'status_manutencao_{manutencao["id"]}'
                )

            tipo_manutencao = st.radio(
                '🛠 Tipo de Manutenção',
                TipoManutencao.listar_tipos_manutencao(),
                format_func=lambda x: x['nome'],
                horizontal=True,
                key=f'tipo_manutencao_{manutencao["id"]}'
                )

            col9, col10 = st.columns(2)
            qtd_horas_mecanico = col9.number_input(
                '⏱️ Horas Previstas de Mecânico',
                format='%d',
                key=f'qtd_horas_mecanico_{manutencao["id"]}',
                value=manutencao['qtd_horas_mecanico'],
                step=1
                )
            tipo_mao_obra = col10.radio(
                '🧑‍🏭 Tipo de Mão de Obra',
                TipoMaoDeObra.listar_tipos_mao_de_obra(),
                format_func=lambda x: x['nome'],
                horizontal=True,
                key=f'tipo_mao_obra_{manutencao["id"]}'
                )

            mecanico = None
            data_inicio = None
            data_termino = None
            resolucao_problema = ''

            if status_manutencao['nome'] in ['INICIADO', 'FINALIZADO']:
                ids_mecanicos_manutencao = manutencao.get('mecanicos', [])
                mecanicos_selecionados = col9.multiselect(
                    '👨‍🔧 Mecânicos Responsáveis',
                    options=Mecanicos.listar_mecanicos(),
                    default=[m for m in Mecanicos.listar_mecanicos() if m['id'] in ids_mecanicos_manutencao],
                    format_func=lambda x: f'{x["nome"]} ({x["cargo"]})',
                    key=f'mecanicos_{manutencao["id"]}'
                )

                data_inicio = col9.date_input(
                    '📆 Início da Manutenção',
                    format='DD/MM/YYYY',
                    value=manutencao['dt_inicio_manutencao'],
                    min_value=manutencao['dt_entrada'],
                    key=f'data_inicio_{manutencao["id"]}',
                    )

            if status_manutencao['nome'] == 'FINALIZADO':
                data_termino = col9.date_input(
                    '🏁 Término da Manutenção',
                    format='DD/MM/YYYY',
                    value=manutencao['dt_termino_manutencao'],
                    min_value=manutencao['dt_entrada'],
                    key=f'data_termino_{manutencao["id"]}',
                    )

                resolucao_problema = st.text_area(
                    '🔧 Resolução do Problema',
                    height=80,
                    value=manutencao.get('problema_resolucao', ''),
                    placeholder='Descreva a resolução do problema',
                    key=f'resolucao_problema_{manutencao["id"]}',
                    )

            descricao_problema = st.text_area(
                '📄 Descrição do Problema Encontrado',
                height=100,
                value=manutencao.get('problema_descricao', ''),
                placeholder='Descreva o problema encontrado',
                key=f'descricao_problema_{manutencao["id"]}',
                )

            observacao = st.text_area(
                '🗒️ Observações',
                height=80,
                value=manutencao.get('observacao', ''),
                placeholder='Adicione observações adicionais',
                key=f'observacao_{manutencao["id"]}',
                )

            col11, col12 = st.columns(2)

            botao_atualizar = col11.button(
                '✅ Atualizar',
                key=f'atualizar_{manutencao["id"]}',
            )

            if botao_atualizar:
                try:
                    Manutencoes.atualizar_manutencao(
                        id=manutencao['id'],
                        status_de_manutencao_id=status_manutencao['id'],
                        patrimonio_id=patrimonio['id'],
                        regional_id=regional['id'],
                        solicitante_id=solicitante['id'],
                        classificacao_de_manutencao_id=manutencao_classificacao['id'],
                        prioridade_id=prioridade['id'] if isinstance(prioridade, dict) else prioridade,
                        tipo_de_manutencao_id=tipo_manutencao['id'],
                        dt_entrada=data_entrada,
                        problema_descricao=descricao_problema,
                        observacao=observacao,
                        mecanicos_ids=[m['id'] for m in mecanicos_selecionados],
                        dt_inicio_manutencao=data_inicio,
                        dt_termino_manutencao=data_termino,
                        tipo_de_mao_de_obra_id=tipo_mao_obra['id'],
                        qtd_horas_mecanico=qtd_horas_mecanico,
                        localidade_id=locais['id'],
                        problema_resolucao=resolucao_problema,
                    )
                    st.success('✅ Atualização salva com sucesso!')
                except Exception as e:
                    st.error(f'❌ Falha ao atualizar manutenção: {e}')

            botao_excluir = col12.button(
                '❌ Excluir',
                key=f'excluir_{manutencao["id"]}',
                on_click=Manutencoes.excluir_manutencao,
                args=(manutencao['id'],)
            )
else:
    st.warning('⚠️ Nenhuma manutenção encontrada com os filtros aplicados.')
