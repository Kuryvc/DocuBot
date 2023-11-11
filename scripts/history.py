import streamlit as st
from scripts.s3 import s3ConnectionSingleton
import PyPDF2
from io import BytesIO

class Response:
    response = ""
    
    @classmethod
    def set_response(self, text):
        self.response = text
    
    @classmethod
    def get_response(self):
        return self.response
    
    @classmethod
    def button_click(self, search_name): #Retrieve from S3

        print(f'{search_name} button clicked')
        # Aquí va lógica para ir por la info de los pdfs y cargarla para ser procesada
        username = st.session_state.username
        s3_connection = s3ConnectionSingleton.getConnection()    
        folder_path = f"users/{username}/{search_name}/"
        
        objects = s3_connection.list_objects_v2(Bucket='docubotbucket', Prefix=folder_path)    
        
        text = ""        
        for object in objects.get('Contents', []):
            file_content = s3_connection.get_object(Bucket='docubotbucket', Key = object['Key'])['Body'].read()
                
            if object['Key'].lower().endswith('.pdf'):
                # Parse PDF content using PyPDF2
                pdf_io = BytesIO(file_content)
                pdf_reader = PyPDF2.PdfReader(pdf_io)
                
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
        self.set_response(text)
    
    


def sidebar_history():
    st.sidebar.header("Búsquedas")

    # Nueva búsqueda
    new_search_title = st.sidebar.text_input("Nueva búsqueda: ")
    
    s3_connection = s3ConnectionSingleton.getConnection()
    username = st.session_state.username
    
    
    if st.sidebar.button("Confirmar") and new_search_title:
        st.session_state.searchSelected = True
        st.session_state.new_search = True
        st.session_state.searchName = new_search_title
        print(st.session_state.searchName)
        #Subir nueva carpeta de la búsqueda a S3 usando el username de session state y el search name de aquí 
        
        s3_connection = s3ConnectionSingleton.getConnection()
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
    
    folder_name = f'users/{username}/'
    #Retrieve all the folders of seraches, their names.
    
    name_set = set()         
    st.sidebar.subheader("Hustorial de búsquedas")
    
    objects = s3_connection.list_objects_v2(Bucket='docubotbucket', Prefix=folder_name)
    
    for object in objects.get('Contents', []):
        name = object['Key'].split('/')[2]
        if name != "":
            name_set.add(name)        
    for element in name_set:
        if st.sidebar.button(f'{element}'):
            st.session_state.searchSelected = True
            st.session_state.old_search = True
            st.session_state.searchName = element
                        
            Response.button_click(element)
            
    # search_list = st.session_state.current_user['Searches']['L']
    # for search in search_list:
    #     element = search['S']
    #     print(element)
        # if st.sidebar.button(f'{element}'):
        #     st.session_state.searchSelected = True            
        #     st.session_state.old_search = True
            
        #     button_click(element)
        
    