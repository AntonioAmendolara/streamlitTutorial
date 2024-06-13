import streamlit as st
from utils.utils import *
import pymysql,cryptography

if __name__ == "__main__":
    st.set_page_config(
        page_title="La mia app",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://dbdmg.polito.it/',
            'Report a bug': "https://dbdmg.polito.it/",
            'About': "# Corso di *Basi di Dati*"
        }
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        st.title(":hotel: Gestione stanze hotel")
        st.markdown("## :red[Laboratorio 6] | Corso :blue[Basi di Dati]")
    with col2:
        st.image("images/polito_white.png")
    
    
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    check_connection()
  