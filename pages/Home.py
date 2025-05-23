import streamlit as st

st.set_page_config(page_title="Sistema Oficina", page_icon="favicon.ico",)

st.title('Controle Oficina')

# Logo ou imagem opcional
st.logo("logobc.png",size='large', icon_image='favicon.ico')

# Título e boas-vindas
st.markdown("""
    <h1 style='text-align: center; color: #333;'>🔧 Sistema de Controle de Manutenções</h1>
    <h4 style='text-align: center; color: gray;'>Organize mecânicos, patrimônios e execuções com precisão</h4>
    <hr style='margin-top:10px;margin-bottom:10px'>
""", unsafe_allow_html=True)

st.markdown("""
### 📚 Menu de Navegação
Utilize a barra lateral para acessar as seções:

- **📥 Entrada de Manutenção**: registre novas solicitações.
- **🛠 Atualizar Manutenções**: altere status, responsáveis e datas.
- **🔧 Cadastro Geral**: insira mecânicos, patrimônios e solicitantes.
- **📊 Relatórios**: visualize métricas e histórico.
- **⚙️ Configurações**: ajuste parâmetros do sistema.

> 💡 Dica: Use o atalho `Ctrl+S` para salvar dados com segurança.
""")