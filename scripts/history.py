import streamlit as st

def sidebar_history():
    st.sidebar.header("Búsquedas")

    # Nueva búsqueda
    new_search_title = st.sidebar.text_input("Nueva búsqueda: ")
    
    if st.sidebar.button("Confirmar") and new_search_title:
        st.session_state.new_search = True
        st.session_state.searchName = new_search_title
        print(st.session_state.searchName)
        #Subir nueva carpeta de la búsqueda a S3
        

    # Nueva búsqueda
    st.sidebar.subheader("Hustorial de búsqueda")
    st.sidebar.button("Búsqueda 1")