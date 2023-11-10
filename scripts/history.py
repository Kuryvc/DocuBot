import streamlit as st
from scripts.s3 import s3ConnectionSingleton


def sidebar_history():
    st.sidebar.header("Búsquedas")

    # Nueva búsqueda
    new_search_title = st.sidebar.text_input("Nueva búsqueda: ")
    
    if st.sidebar.button("Confirmar") and new_search_title:
        st.session_state.new_search = True
        st.session_state.searchName = new_search_title
        print(st.session_state.searchName)
        #Subir nueva carpeta de la búsqueda a S3 usando el username de session state y el search name de aquí 
        
        s3_connection = s3ConnectionSingleton.getConnection()
        username = st.session_state.username
        folder_name = f'users/{username}/{new_search_title}/'
        
        try:
            s3_connection.head_object(Bucket='docubotbucket', Key=folder_name)
            st.warning(f"The folder '{folder_name}' already exists.")
        except Exception as e :
            if e.response['Error']['Code'] == '404':
                # The folder doesn't exist; create the user folder in the S3 bucket
                s3_connection.put_object(Bucket='docubotbucket', Key=folder_name)
            else:
                print(f"An error occurred: {e}")     
        

    # Nueva búsqueda
    st.sidebar.subheader("Hustorial de búsquedas")
    # print(st.session_state.current_user['Searches']['L']) 
    search_list = st.session_state.current_user['Searches']['L']
    for search in search_list:
        element = search['S']
        st.sidebar.button(f'{element}')
        print(search['S'])
    