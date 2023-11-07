import streamlit as st
import json
import bcrypt

def hash_password(password):
    # Genera una sal (salt) aleatoria para aumentar la seguridad
    salt = bcrypt.gensalt()
    
    # Hashea la contraseña utilizando la sal
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password


def check_password(entered_password, hashed_password):
    if isinstance(entered_password, str):
        entered_password = entered_password.encode('utf-8')  # Codifica la cadena a bytes

    return bcrypt.checkpw(entered_password, hashed_password)


def register(username, password):
    with open('user_data.json', 'r') as user_data_file:
        user_data = json.load(user_data_file)

    if username not in user_data:
        # Asegúrate de hashear la contraseña antes de guardarla
        hashed_password = hash_password(password)  # Utiliza tu función hash_password
        user_data[username] = {'password': hashed_password.decode('utf-8'), 'searches': {}}

        with open('user_data.json', 'w') as user_data_file:
            json.dump(user_data, user_data_file)
        
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.chat_history = []
        return True
    else:
        st.warning("El usuario ya existe.")
        return False


def login(username, password):
    with open('user_data.json', 'r') as user_data_file:
        user_data = json.load(user_data_file)

    user_info = user_data.get(username, {})
    stored_password_hash = user_info.get('password', '').encode('utf-8')  # Convierte a bytes

    if user_info and check_password(password, stored_password_hash):
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.chat_history = []
        # return True
    else:
        st.warning("Usuario o contraseña incorrecta.")
        # return False



def sidebar_login():
    st.sidebar.header("Inicio de sesión/Registro")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")

    if st.sidebar.button("Login"):
        login(username, password)

    if st.sidebar.button("Registrar"):
        register(username, password)