from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from scripts.s3 import s3ConnectionSingleton
import streamlit as st
from io import BytesIO

def upload_pdf_toS3(pdf_docs):
    
    s3_connection = s3ConnectionSingleton.getConnection()
    userName = st.session_state.username
    searchName = st.session_state.searchName
    
    folder_name = f'users/{userName}/{searchName}/'
    
    for pdf in pdf_docs:
        filename = pdf.name
        folder_name += filename
        
        try:
            s3_connection.upload_fileobj(BytesIO(pdf.read()), 'docubotbucket', folder_name) 
            print (f'File: {filename} uploaded')            
        except Exception as e:
            st.error('An error ocurred, couldn´t upload your files to S3, but your search will still be processed for you to ask')
             
def get_pdf_text(pdf_docs): #pfdocs contains one or more pdf files
    text = ""
    for pdf in pdf_docs: #loop through pdfs
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages: # loop through pages on current pdf_reader
            text += page.extract_text()
    return text

def get_text_chunks(pdf_text):
    text_splitter = CharacterTextSplitter(separator="\n", 
                                          chunk_size = 1000, 
                                          chunk_overlap = 200,
                                          length_function = len)
    chunks = text_splitter.split_text(pdf_text)
    return chunks
