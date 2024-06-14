import streamlit as st
import pandas as pd
from utils.utils import *
#Creazione di una pagina per la visualizzazione e filtraggio dei corsi disponibili. 
#La pagina deve essere supportata da due metric per mostrare il numero di corsi e di tipi distinti disponibili.
#  
#I widget di input devono essere creati in modo da proporre come opzioni le informazioni contenute già a database. 
#L’utente deve poter visualizzare le informazioni sui corsi filtrando per più categorie (i.e., Tipo) e deve poter specificare 
#il range di livello a cui è interessato. 
# 
# In un expander separato, visualizzare i programmi delle lezioni per i corsi selezionati
#e nome e cognome dell’istruttore corrispondente. In caso di risultati vuoti, bisogna stampare un errore/warning associato. 

if __name__ == "__main__":
    
    st.set_page_config(
        page_title="Corsi",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    if check_connection():
        st.title(":clipboard: Corsi")
        col1, col2 = st.columns(2)
        with col1:
            query = "SELECT COUNT(CodC) AS N FROM corsi"
            NumeroCorsi = execute_query(st.session_state["connection"], query)
            st.metric("Corsi disponibili", NumeroCorsi.mappings().first()["N"])

        with col2:
            query = "SELECT COUNT(DISTINCT(Tipo)) AS T FROM corsi"
            NumeroTipi = execute_query(st.session_state["connection"], query)
            st.metric("Tipi di corsi disponibili", NumeroTipi.mappings().first()["T"])

        #------------------------------- filtri -------------------------------------------
        option = st.multiselect("Seleziona le categorie di filtraggio", ["Nome", "Tipo", "Livello"])
        queryNome = ""
        queryTipo = ""
        queryRange = ""

        if "Nome" in option:
            listaNomi = getList("Nome", "corsi")
            filtroNome = st.selectbox("Filtra per il nome dell'istruttore", listaNomi)
            queryNome = f" AND C.Nome = \"{filtroNome}\""
        if "Tipo" in option:
            listaTipo = getList("Tipo", "corsi")
            filtroTipo = st.selectbox("Filtra per il tipo del corso", listaTipo)
            queryTipo = f" AND C.Tipo = \"{filtroTipo}\""
        if "Livello" in option:
            queryMAX = f"SELECT MAX(Livello) AS MAX FROM corsi"
            queryMIN = f"SELECT MIN(Livello) AS MIN FROM corsi"
            max = execute_query(st.session_state["connection"], queryMAX)
            min = execute_query(st.session_state["connection"], queryMIN)
            MIN = min.mappings().first()["MIN"]
            MAX = max.mappings().first()["MAX"]
            range = st.slider("Seleziona il range di livello desiderato", MIN, MAX, (1, 2))
            st.write("Range selezionato:", range)
            queryRange = f" AND C.Livello <= {int(range[1])} AND C.Livello >= {int(range[0])}"

        queryData = f"SELECT I.Nome, I.Cognome, P.* FROM corsi C, programma P, istruttore I WHERE C.CodC = P.CodC AND P.CodFisc = I.CodFisc{queryRange}{queryNome}{queryTipo}"
        res = execute_query(st.session_state["connection"], queryData)
        tabellaCorsi = pd.DataFrame(res)
        
        with st.expander(":pushpin: Elenco Programmi", True):
            if tabellaCorsi.empty:
                st.info(":information_source: Non è prensente alcun risultato che soddisfi i parametri inseriti :sob:")
            else:
                table = st.dataframe(tabellaCorsi, use_container_width=True)