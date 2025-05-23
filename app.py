import streamlit as st


# st.set_page_config(page_title="Sistema Oficina", page_icon="favicon.ico",)

st.logo("logobc.png",size='large', icon_image='favicon.ico')


pg = st.navigation(
    {
        'Início':[
            st.Page("pages/Home.py", title="Início", icon="🏠"),
            ], 
        'Gerenciar Manutenções':[
            st.Page('pages/Entrada_de_manutencao.py', title='Entrada de Manutenção', icon='📥'),
            st.Page('pages/Atualizar_manutencao.py', title='Atualizar Manutenção', icon='🛠'),
            st.Page("pages/Relatórios.py", title="Relatórios", icon="📊") 
            ],
        'Cadastro':[
            st.Page('pages/Cadastro.py', title='Cadastro Geral', icon='🔧'),
            st.Page('pages/Configurações.py', title='Configurações', icon='⚙️')
            ],
    }
)

pg.run()