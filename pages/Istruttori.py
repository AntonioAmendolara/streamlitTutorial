# Creazione di una pagina per la visualizzazione degli istruttori disponibili. 
# L’utente deve avere la possibilità di filtrare digitando il cognome dell’istruttore e utilizzando un date range 
# per scegliere in base alla data di nascita (hint: usare datetime.date() per impostare il date_input e passare la data 
# come stringa nell’interrogazione). La visualizzazione non deve essere una tabella complessiva, 
# ma divisa elemento per elemento (creare un dataframe e usare df.iterrows per stampare una row alla volta, vedi Lab 6). 
# Aggiungere un’icona per ogni risultato. In caso di risultati vuoti, bisogna visualizzare un messaggio associato. 

import streamlit as st
import datetime as dt
import pandas as pd
from utils.utils import *

if __name__ == "__main__":

    st.set_page_config(
        page_title="Istruttori",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if check_connection():
        st.title(":moyai: Istruttori")

        filtro = st.radio("Attraverso quale filtro vuoi selezionare gli istruttori?", ["Cognome", "Data di nascita"], horizontal=True)

        if filtro == "Cognome":
            cognomi = getList("Cognome", "istruttore")
            surname = st.selectbox("Scegli l'istruttore da te desiderato", cognomi)
            query = f"SELECT * FROM istruttore WHERE istruttore.Cognome = '{surname}'"
        if filtro == "Data di nascita":
            data = st.date_input("Seleziona la data di nascita", dt.date(1980, 1, 1))
            query = f"SELECT * FROM istruttore WHERE istruttore.DataNascita = '{data}'"
        
        result = execute_query(st.session_state["connection"], query)
        dataRes = pd.DataFrame(result)

        if dataRes.empty:
            st.info(":rotating_light: Nessun risultato")
        for index, row in dataRes.iterrows():
            st.write(":alien:")
            st.write(f":green[Codice Fiscale:] {row['CodFisc']}")
            st.write(f":green[Nome:] {row['Nome']}")
            st.write(f":green[Cognome:] {row['Cognome']}")
            st.write(f":green[Data di nascita:] {row['DataNascita']}")
            st.write(f":green[Email:] {row['Email']}")
            st.write(f":green[Telefono:] {row['Telefono']}")
            st.write("--------------------------------------------------")

        