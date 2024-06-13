import streamlit as st
from utils.utils import *

def getList(tab, attributo):
    # funzione in grado di prelevare una lista dei valori distinti di un attributo dal una determinata tabella
    # entrambi specificati in input
    query = f"SELECT DISTINCT({attributo}) FROM {tab};"
    result = execute_query(st.session_state["connection"], query)
    result_list = []
    for row in result.mappings(): # serve a trasformare lista di tuple in lista di dizionari
        result_list.append(row[attributo])
    
    return result_list

def map_optional(optional):
    query = ""
    for element in optional:
        query=query+(f" AND HO.OPTIONAL_Optional='{element}'")
    return query



if __name__ == "__main__":
    st.title("Stanze")
    #Impostare un expander “Filtri” da cui l’utente possa selezionare le opzione preferite per il filtraggio delle stanze disponibili: 
    #il tipo (singola, doppia, tripla, tutte) con un radio button, 
    #gli optional con un multiselect, 
    #se è presente la cucina tra gli spazi disponibili con un checkbox

    if check_connection():
        with st.expander("Filtri", expanded= True):
            col1, col2, col3 = st.columns(3)

            col1.radio("Che tipo di stanza cerchi?", ["singola", "doppia", "tripla" , "tutte"])
            
            optionalList = getList("has_optional", "OPTIONAL_optional")
            col2.multiselect("Optional: ", optionalList)

            cucinaFlag = col3.checkbox("Cucina inclusa tra gli spazi")

            optionalQuery=map_optional(optionalList)
            typeQuery=f"AND S.Type ={type}" if type!='Tutte' else ''
            st.write(optionalQuery)

            if cucinaFlag:
                st.write("Cucina inclusa negli spazi disponibili")
                query = f"SELECT * FROM STANZA S, HAS_SPAZI HS, HAS_OPTIONAL HO WHERE S.CodS = HS.STANZA_CodS AND HO.CodS = S.CodS AND {typeQuery} {optionalQuery} AND SPAZI_Spazi = 'cucina'"
            else:
                st.write("Cucina :red[non] inclusa negli spazi disponibili")
                query = f"SELECT * FROM STANZA S, HAS_SPAZI HS, HAS_OPTIONAL HO WHERE S.CodS = HS.STANZA_CodS AND HO.CodS = S.CodS AND {typeQuery} {optionalQuery}"
            
            res = execute_query(st.session_state["connection"], query)