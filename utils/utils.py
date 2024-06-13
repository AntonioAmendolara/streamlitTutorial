import streamlit as st
from sqlalchemy import create_engine, text

#Connessione all'engine
def connect_db(dialect, username, password, host, dbname):
    try:
        engine= create_engine(f'{dialect}://{username}:{password}@{host}/{dbname}')
        conn = engine.connect()
        return conn
    except:
        return False

def execute_query(conn, query):
    return conn.execute(text(query))

#controllo connessione
def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    if st.sidebar.button("Connettiti al Database"):
        myconnection = connect_db("mysql+pymysql", "root", "", "localhost", "palestra")
        if myconnection is not False:
            st.session_state["connection"] = myconnection
        else:
            st.session_state["connection"] = False
            st.sidebar.error("Errore di connessione")

    if st.session_state["connection"]:
        st.sidebar.success("Connessione riuscita")
        return True
    
#raccoglie lista dei valori assunti da un attributo in una determinata tabella
def getList(attributo, tab):
    query =f"SELECT DISTINCT {attributo} FROM {tab}"
    result = execute_query(st.session_state["connection"], query)
    res_list = []
    for row in result.mappings():
        res_list.append(row[attributo])
    
    return res_list