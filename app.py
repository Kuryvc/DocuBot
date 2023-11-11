import streamlit as st
from dotenv import load_dotenv
import boto3
import os

# Importando las funciones de los nuevos archivos
from scripts.pdf_processing import get_pdf_text, get_text_chunks, upload_pdf_toS3
from scripts.vectorization import get_vector_index
from scripts.conversation import get_conversation_chain, handle_question
from htmlTemplate import css
from scripts.login import sidebar_login
from scripts.history import sidebar_history, Response
from scripts.s3 import s3_connection, s3ConnectionSingleton


def main():
    load_dotenv()

    st.set_page_config(page_title="Chat with your files", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "new_search" not in st.session_state:
        st.session_state.new_search = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None 
    if "searchName" not in st.session_state:
        st.session_state.searchName = None 
    if "old_search" not in st.session_state:
        st.session_state.old_search = False
    if "searchSelected" not in st.session_state:
        st.session_state.searchSelected = False
        
    s3_connection = s3ConnectionSingleton.getConnection()

    # for bucket in s3_connection.buckets.all():
    #     print(bucket.name)

    with st.sidebar:
        if not st.session_state.searchSelected:
            sidebar_history()
        else:
            
            if "username" in st.session_state:
                st.sidebar.subheader(f"Bienvenido, {st.session_state.username}!")
            #Cuando haya elegido new search
            
            if st.session_state.new_search:
                st.subheader(f'Selecciona tus documentos de la nueva búsqueda: "{st.session_state.searchName}"')
                pdf_docs = st.file_uploader("Sube tus archivos PDF y haz clic en procesar ",accept_multiple_files=True)
            
            elif st.session_state.old_search:
                st.subheader(f'Sus documentos de las búsqueda "{st.session_state.searchName}" se han cargado. Haga click en procesar para comenzar a preguntar')
                                

            if st.button("Procesar"):
                with st.spinner("Procesando"):
                    
                    if st.session_state.new_search:
                        upload_pdf_toS3(pdf_docs);     
                        extracted_text = get_pdf_text(pdf_docs)
                    elif st.session_state.old_search:
                        extracted_text = Response.get_response()
                    
                    text_chunks = get_text_chunks(extracted_text)
                    print(text_chunks)
                    vector_store = get_vector_index(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vector_store)
                                
    st.header("Chat con tus archivos :books:")
    user_question = st.text_input("Haz una pregunta acerca de tus documentos:")

    if user_question:
        handle_question(user_question)


if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = None    
        
    if not st.session_state.authenticated:
        sidebar_login()
    else:
        main()
