import streamlit as st
import numpy as np
import pandas as pd
from utils.utils import *

st.set_page_config(
    page_title="BDD/Quaderno 4",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://dbdmg.polito.it/',
        'Report a bug': "https://dbdmg.polito.it/",
        'About': "# Quaderno 4*"
    }
)

col1, col2 = st.columns([5, 1])
with col1:
    st.title("Corso :blue[Basi di Dati] | Quaderno :green[4]")
    st.markdown("## Sviluppo di un'applicazione Web con :red[Streamlit] e :orange[MySQL]")
    st.markdown("#### S311977 | Amendolara Antonio")
with col2:
    st.image("images/polito_white.png")

if check_connection():
    c1, c2 = st.columns(2)
    with c1:
        #Bar Chart che riporti il numero di lezioni per ogni slot di tempo
        lista_orari = getList("OraInizio", "programma")
        query = "SELECT COUNT(*) AS Numero_Lezioni FROM programma GROUP BY OraInizio"
        data = execute_query(st.session_state["connection"], query)
        dt = pd.DataFrame(data, lista_orari)
        st.bar_chart(dt)

    with c2:
        #Area Chart che riporti il numero di lezioni programmate in base al giorno della settimana
        lista_lezioni = getList("Giorno", "programma")
        query = "SELECT COUNT(*) AS Numero_Lezioni FROM programma GROUP BY Giorno"
        dati_settimana = execute_query(st.session_state["connection"], query)
        dati = pd.DataFrame(dati_settimana, lista_lezioni)

        st.area_chart(dati)
