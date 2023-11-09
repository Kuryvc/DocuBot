import streamlit as st
from dotenv import load_dotenv
import boto3
import os

# Importando las funciones de los nuevos archivos
from scripts.pdf_processing import get_pdf_text, get_text_chunks
from scripts.vectorization import get_vector_index
from scripts.conversation import get_conversation_chain, handle_question
from htmlTemplate import css
from scripts.login import sidebar_login
from scripts.history import sidebar_history


def main():
    load_dotenv()

    st.set_page_config(page_title="Chat with your files", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "new_search" not in st.session_state:
        st.session_state.new_search = None
    if "current_user" not in st.session_state:
        st.session_state.new_search = None 
    if "searchName" not in st.session_state:
        st.session_state.searchName = None 

    s3 = boto3.resource(
        service_name="s3",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    for bucket in s3.buckets.all():
        print(bucket.name)

    with st.sidebar:
        # print(st.session_state.new_search)
        if not st.session_state.new_search:
            sidebar_history()
        else:
            if "username" in st.session_state:
                st.sidebar.subheader(f"Bienvenido, {st.session_state.username}!")
            st.subheader("Selecciona tus documentos")
            pdf_docs = st.file_uploader(
                "Sube tus archivos PDF y haz clic en procesar",
                accept_multiple_files=True,
            )

            if st.button("Procesar"):
                with st.spinner("Procesando"):
                    extracted_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(extracted_text)
                    vector_store = get_vector_index(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vector_store)
        # else:
        #     if "username" in st.session_state:
        #         st.sidebar.subheader(f"Bienvenido, {st.session_state.username}!")
        #     st.subheader("Selecciona tus documentos")
        #     pdf_docs = st.file_uploader("Sube tus archivos PDF y haz clic en procesar", accept_multiple_files=True)

        #     if st.button("Procesar"):
        #         with st.spinner("Procesando"):
        #             extracted_text = get_pdf_text(pdf_docs)
        #             text_chunks = get_text_chunks(extracted_text)
        #             vector_store = get_vector_index(text_chunks)
        #             st.session_state.conversation = get_conversation_chain(vector_store)

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
