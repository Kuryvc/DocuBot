from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

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
