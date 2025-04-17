import datetime
import streamlit as st

def formatar_data(data: str) -> datetime.date:
    try:
        data =  datetime.datetime.strptime(data, '%Y-%m-%d').date()
        return data.strftime('%d/%m/%Y')
    except ValueError:
        st.error("Erro ao formatar data")
        return None