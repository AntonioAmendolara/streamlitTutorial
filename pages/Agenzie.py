import streamlit as st
from utils.utils import *
import pandas as pd

#ogni tab ha una funzione separata

if __name__ == "__main__":
    st.title(":department_store: Agenzie")

    if check_connection():
        #Utilizzare 3 widget Metric per rappresentare: numero di agenzie distinte salvate a database, 
        #numero di città distinte, nome della città con più agenzie registrate
        col1, col2, col3 = st.columns(3)

        query = "SELECT COUNT(*) AS 'NumeroAgenzie' FROM agenzia;"
        num_ag = execute_query(st.session_state["connection"], query)
        query = "SELECT COUNT(DISTINCT(Citta_Indirizzo)) AS 'NumeroCittà' FROM agenzia;"
        num_cit = execute_query(st.session_state["connection"], query)
        query = "SELECT Citta_Indirizzo, COUNT(*) AS 'QTA' FROM agenzia GROUP BY Citta_Indirizzo ORDER BY QTA DESC;"
        city = execute_query(st.session_state["connection"], query)

        col1.metric("Numero Agenzie", num_ag.mappings().first()['NumeroAgenzie'])
        col2.metric("Numero Città", num_cit.mappings().first()['NumeroCittà'])
        col3.metric("Città con più agenzie", city.mappings().first()['Citta_Indirizzo'])

        #--------------------
        #mappa
        query = "SELECT A.Citta_Indirizzo, C.Latitudine AS 'LAT', C.Longitudine AS 'LON' FROM agenzia A, citta C WHERE C.Nome = A.Citta_Indirizzo"
        città_geo = execute_query(st.session_state["connection"], query)
        df_mappa= pd.DataFrame(città_geo)

        st.map(df_mappa)

        #-----------------------
        #Tabella per le informazioni delle agenzie
        #con filtro per città
        città_cercata = st.text_input("Filtro Città", placeholder="Inserisci la città di interesse")
        if città_cercata == '':
            query = "SELECT Citta_Indirizzo AS 'Città', CONCAT(Via_Indirizzo , ', ',Numero_Indirizzo , ', CAP ',CAP_Indirizzo) AS 'Indirizzo' FROM agenzia;"
        else:
            query = f"SELECT Citta_Indirizzo AS 'Città', CONCAT(Via_Indirizzo , ', ',Numero_Indirizzo , ', CAP ',CAP_Indirizzo) AS 'Indirizzo' FROM agenzia WHERE Citta_Indirizzo = '{città_cercata}'"
        
        indirizzi_agenzie = execute_query(st.session_state["connection"], query)
        df_indirizzi = pd.DataFrame(indirizzi_agenzie)
        st.dataframe(df_indirizzi, use_container_width= True)