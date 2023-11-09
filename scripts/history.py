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
        
        bucket = s3_connection.Bucket('docubotbucket')
        folder_name = f'users/{username}/{new_search_title}/'
        folder_exists = False

        for obj in bucket.objects.filter(Prefix=folder_name):
            if obj.key == folder_name:
                folder_exists = True
                break

        if folder_exists:
            print(f"The folder with the serach name: '{folder_name}' already exists.")
        else:
            # The folder doesn't exist; create the user folder in the S3 bucket
            s3_connection.Object('docubotbucket', folder_name).put()
        
        

    # Nueva búsqueda
    st.sidebar.subheader("Hustorial de búsqueda")
    st.sidebar.button("Búsqueda 1")