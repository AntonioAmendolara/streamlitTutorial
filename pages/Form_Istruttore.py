#Creazione di una pagina per l’inserimento di nuovi istruttori attraverso un form adatto. 
#Usare un form d’inserimento che richiede tutti i dati necessari all’inserimento di un nuovo istruttore
#nella base di dati (CodFisc, Nome, Cognome, DataNascita, Email, Telefono). L’applicazione deve verificare che tutti 
#i campi siano valorizzati tranne il Telefono in quanto opzionale (hint: convertire la data in stringa). 
#In caso di dati mancanti, chiave duplicata o altri errori, l’applicazione deve generare un messaggio d’errore. 
#Se invece i dati inseriti sono corretti e l’operazione d’inserimento va a buon fine, si deve visualizzare un messaggio 
#di corretto inserimento.
import streamlit as st
import datetime
from utils.utils import *

if __name__ == "__main__":
    st.set_page_config(
        page_title="Insert Intructor",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if check_connection():
        with st.form("form", clear_on_submit=False):
            ok = 1  # in questo modo se non ho compilato tutto non va il submit
            st.subheader("Form inserimento nuovi istruttori")

            CF = st.text_input("Codice Fiscale",placeholder="obbligatorio")
            Nome = st.text_input("Nome", placeholder="obbligatorio")
            Cognome = st.text_input("Cognome", placeholder="obbligatorio")
            data = st.date_input("Data di nascita", value=datetime.datetime(1980, 1, 1))
            email = st.text_input("Email", placeholder="obbligatorio")
            telefono = st.text_input("Numero di telefono*", placeholder="facoltativo")

            submit = st.form_submit_button("Submit")
        
        if ((CF == "") | (Nome == "") | (Cognome == "") | (data == "") | (email == "")) & submit:
                st.error("Non hai compilato tutti i campi")
                ok = 0

        if submit & ok:
            query = f"INSERT INTO istruttore(CodFisc, Nome, Cognome, DataNascita, Email, Telefono) VALUES('{CF}', '{Nome}', '{Cognome}', '{data}', '{email}', '{telefono}')"
            execute_query(st.session_state["connection"], query)
            
            st.success("Hai inserito questo istruttore:")
            st.write(":gem:")
            st.write(f":green[Codice Fiscale:] '{CF}'")
            st.write(f":green[Nome:] '{Nome}'")
            st.write(f":green[Cognome:] '{Cognome}'")
            st.write(f":green[Data di nascita:] '{data}'")
            st.write(f":green[Email:] '{email}'")
            st.write(f":green[Telefono:] '{telefono}'")
            st.write("--------------------------------------------------")