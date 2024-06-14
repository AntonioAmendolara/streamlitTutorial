# Creazione di un form per l’inserimento di una nuova lezione settimanale nella tabella PROGRAMMA. 
# 
# Il form deve permettere di inserire tutti i campi necessari (CodFisc, Giorno, OrarioInizio, Durata, CodC, Sala) 
# relativi alla programmazione di una nuova lezione. La selezione dell’istruttore deve avvenire tramite un menù a tendina
# contenente il codice fiscale dei possibili istruttori generato dal contenuto della tabella della base di dati. 
# In modo analogo, anche la selezione del corso deve avvenire tramite un menù a tendina popolato dalla base di dati. 
# 
# Gli altri campi sono invece campi popolati manualmente dall’utente, utilizzando i widget più adatti 
# (e.g., slider per OraInizio e Durata) o quelli testuali. L’applicazione delle verificare che l’utente non cerchi di 
# inserire nel programma lezioni che durino più di 60 minuti e che il giorno indicato sia un giorno compreso tra Lunedì e Venerdì. 
# L’inserimento di una nuova lezione in programma deve essere consentito ed eseguito se e solo se non sono in programma 
# altre lezioni per lo stesso corso nello stesso giorno della settimana (hint: utilizzare i valori di input per effettuare 
# l’interrogazione e verificare che non ci siano record). 
# 
# Se la richiesta di inserimento rispetta i vincoli indicati e l’inserimento termina correttamente, 
# si deve visualizzare un messaggio di corretto inserimento, altrimenti si deve 
# notificare un messaggio d’errore (il messaggio d’errore deve riportare il tipo di problema che ha comportato l’errore)

def insert_lezione(i, d, h, durata, c, s):
    st.success("Hai inserito questa lezione:")
    st.write(":gem:")
    st.write(f":green[Codice Fiscale Istruttore:] '{i}'")
    st.write(f":green[Giorno:] '{d}'")
    st.write(f":green[Ora di inizio:] '{h}'")
    st.write(f":green[Durata:] '{durata}'")
    st.write(f":green[Codice corso:] '{c}'")
    st.write(f":green[Sala:] '{s}'")
    st.write("--------------------------------------------------")


import streamlit as st
import datetime
import pandas as pd
from utils.utils import *

if __name__ == "__main__":
    st.set_page_config(
        page_title="Form Lezione",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if check_connection():
        dayList = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
        istrList = getList("Cognome", "istruttore")
        CorsoList = getList("Nome", "corsi")
        
        with st.form("form", clear_on_submit=False):
            ok = 1
            st.subheader("Form inserimento nuova lezione")

            istruttore = st.selectbox("Scegli il tuo istruttore", istrList)
            corso = st.selectbox("Scegli il tuo corso", CorsoList)
            giorno = st.selectbox("Scegli in che giorno prenotare la lezione", dayList)
            durata = st.slider("Imposta la durata in minuti della lezione", 0, 60)
            sala = st.text_input("Inserisci la sala in cui vuoi prenotare la lezione")
            oraInizio = st.slider("Scegli a che ora vuoi iniziare", value=datetime.time(9, 0), format = "HH:mm",)

            submit = st.form_submit_button("submit")
        
        if submit:
            if not sala:
                ok = 0
                st.error(":rotating_light: Non hai completato tutti i campi!")
            
            #cerco se ci sono altre occorrenze nello slot richiesto
            query = f"SELECT * FROM programma P, corsi C WHERE P.CodC = C.CodC AND P.Giorno = '{giorno}' AND  C.Nome = '{corso}'"
            coincidenze = execute_query(st.session_state["connection"], query)
            dt = pd.DataFrame(coincidenze)
            if dt.empty & ok:
                #prendo codice fiscale e codice corso
                queryIstruttore = f"SELECT CodFisc AS I FROM istruttore WHERE Cognome = '{istruttore}'"
                queryCorso = f"SELECT CodC AS C FROM corsi WHERE Nome = '{corso}'"
                codIstr = execute_query(st.session_state["connection"], queryIstruttore)
                codCorso = execute_query(st.session_state["connection"], queryCorso)

                codIstr = codIstr.mappings().first()["I"]
                codCorso = codCorso.mappings().first()["C"]

                query = f"INSERT INTO programma(CodFisc, Giorno, OraInizio, Durata, CodC, Sala) VALUES('{codIstr}', '{giorno}', '{oraInizio}', '{durata}', '{codCorso}', '{sala}')"
                execute_query(st.session_state["connection"], query)
                insert_lezione(codIstr, giorno, oraInizio, durata, codCorso, sala)
            elif (not dt.empty):
                st.error(":rotating_light: Slot già occupato)")

