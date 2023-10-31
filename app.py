import streamlit as st
from dotenv import load_dotenv
import os

# Importando las funciones de los nuevos archivos
from scripts.pdf_processing import get_pdf_text, get_text_chunks
from scripts.vectorization import get_vector_index
from scripts.conversation import get_conversation_chain, handle_question
from htmlTemplate import css, bot_template, user_template

# Placeholder para estructura de datos
users_data = {
    'username': {   # Nombre del usuario
        'password': 'hashed_password',  # Contraseña del usuario (encriptada)
        'searches': {  # Historial de búsquedas del usuario
            'search_name': {   # Nombre o identificador de una búsqueda específica
                'text_chunks': [],  # Fragmentos de texto relacionados con esa búsqueda
                'vector_store': None  # Información vectorizada (por ejemplo, para búsquedas rápidas o análisis)
            }
        }
    }
}
def register(username, password):
    if username not in users_data:
        # Asegúrate de hashear la contraseña antes de guardarla
        hashed_password = password  # Deberías cambiar esto por una función de hashing real
        users_data[username] = {'password': hashed_password, 'searches': {}}
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.chat_history = []
        return True
    else:
        st.warning("El usuario ya existe.")
        return False

def login(username, password):
    user_data = users_data.get(username, {})
    hashed_password = password  # Cambia esto por una función de hashing real
    if user_data and user_data['password'] == hashed_password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.chat_history = []
        return True
    else:
        st.warning("Usuario o contraseña incorrecta.")
        return False

def sidebar_login():
    st.sidebar.header("Inicio de sesión/Registro")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")

    if st.sidebar.button("Login"):
        login(username, password)

    if st.sidebar.button("Registrar"):
        register(username, password)
        
def main():
    load_dotenv()
    
    st.set_page_config(page_title="Chat with your files", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    with st.sidebar:
        if "username" in st.session_state:
            st.sidebar.subheader(f"Bienvenido, {st.session_state.username}!")
        st.subheader("Selecciona tus documentos")
        pdf_docs = st.file_uploader("Sube tus archivos PDF y haz clic en procesar", accept_multiple_files=True)
        
        if st.button("Procesar"):
            with st.spinner("Procesando"):
                extracted_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(extracted_text)
                vector_store = get_vector_index(text_chunks)
                st.session_state.conversation = get_conversation_chain(vector_store)
        
    
    st.header("Chat con tus archivos :books:")
    user_question = st.text_input("Haz una pregunta acerca de tus documentos:")
    
    if user_question:
        handle_question(user_question)

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        
    if not st.session_state.authenticated:
        sidebar_login()
    else:
        main()