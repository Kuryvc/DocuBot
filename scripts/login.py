import streamlit as st
import json
import bcrypt
from scripts.db import dynamoConnectionSingleton
from scripts.s3 import s3ConnectionSingleton
    

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
    
    #Verify thers no other equal username
    response = dbconnection.get_item(
        TableName='docuBotUsers',
        Key={'userId': {'S': username}}
    )    

    #If no other user withe the same username already exists, then register
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
        
        #create user folder en s3 bucket
        s3_connection = s3ConnectionSingleton.getConnection()
        folder_name = f'users/{username}/'
        
        try:
            s3_connection.head_object(Bucket='docubotbucket', Key=folder_name)
            st.warning(f"The folder '{folder_name}' already exists.")
        except Exception as e :
            if e.response['Error']['Code'] == '404':
                # The folder doesn't exist; create the user folder in the S3 bucket
                s3_connection.put_object(Bucket='docubotbucket', Key=folder_name)
            else:
                print(f"An error occurred: {e}")      
    
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

    if st.sidebar.button("Login") and username and password:
        try:
            login(username, password)
        except Exception as e :
            st.warning("Error al registrar usuario")
            print(e)

    if st.sidebar.button("Registrar") and username and password:
        try:
            if register(username, password):
                st.warning("Se ha creado el usuario con éxito. Ahora puede iniciar sesión")
        except Exception as e :
            st.warning("Error al registrar usuario")
            print(e)