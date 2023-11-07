import streamlit as st

def sidebar_history():
    st.sidebar.header("Búsquedas")

    # Nueva búsqueda
    new_search_title = st.sidebar.text_input("Nueva búsqueda: ")
    if st.sidebar.button("Confirmar") and new_search_title:
        st.session_state.new_search = True

    # Nueva búsqueda
    st.sidebar.subheader("Hustorial de búsqueda")
    st.sidebar.button("Búsqueda 1")