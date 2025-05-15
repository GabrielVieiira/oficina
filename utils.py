import datetime
import streamlit as st
from typing import Optional

def formatar_data(data: str) -> Optional[str]:
    try:
        data_obj =  datetime.datetime.strptime(data, '%Y-%m-%d').date()
        return data_obj.strftime('%d/%m/%Y')
    except ValueError:
        # st.error("Erro ao formatar data")
        return None
    
data_str = '2025-05-15'
data_formatada = formatar_data(data_str)

if data_formatada:
    print(f"Data formatada: {data_formatada}")
    