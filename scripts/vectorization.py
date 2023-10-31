from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores.faiss import FAISS

def get_vector_index(text_chunks): 
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectoreStore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectoreStore
