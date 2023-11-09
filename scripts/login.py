import streamlit as st
import json
import bcrypt
from scripts.db import dynamo_connection, dynamoConnectionSingleton
    

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
    dbconnection = dynamoConnectionSingleton.getConnection()
    
    response = dbconnection.get_item(
        TableName='docuBotUsers',
        Key={'userId': {'S': username}}
    )    

    if 'Item' not in response:
        # Asegúrate de hashear la contraseña antes de guardarla
        hashed_password = hash_password(password)  # Utiliza tu función hash_password
    
        dbconnection.put_item(
            TableName='docuBotUsers',
            Item={
                'userId': {'S': username},
                'Username': {'S': username}, # 'S' es tipo string.
                'Password': {'S': str(hashed_password, 'utf-8')},
                'Searches': {'L': []}  # Initialize with an empty list. 'L' es tipo lista
        })
                
        # st.session_state.authenticated = True
        st.session_state.username = username
        return True
    else:
        st.warning("El usuario ya existe.")
        return False

def login(username, password):
    
    dbconnection = dynamoConnectionSingleton.getConnection()
    
    response = dbconnection.get_item(
        TableName='docuBotUsers',
        Key={'userId': {'S': username}}
    )
    
    item = response.get('Item') #El response trae la info del usuario en el key 'Item'
    print(item.get('Password')['S'])
    
    storedPassword = item.get('Password', {}).get('S')
    
    if item and check_password(password, storedPassword.encode('utf-8')):
        st.session_state.authenticated = True
        st.session_state.username = username #this will be used to create the folders of every user
        st.session_state.current_user = item
        
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
        if register(username, password):
            st.warning("Se ha creado el usuario con éxito. Ahora puede iniciar sesión")
            
        # print(st.session_state.current_user)
        
    # def authenticate_user(username, password):
    #     response = dynamodb.get_item(
    #     TableName='tablaDeUsuarios',
    #     Key={'Username': {'S': username}}
    # )
    # item = response.get('Item') #El response trae la info del usuario en el key 'Item'

    # if item and item.get('Password', {}).get('S') == password:
    #     return True
    # else:
    #     return False