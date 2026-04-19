from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

def get_embeddings():
    """Returns the default embedding model."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_vectorstore(file_path: str, persist_directory: str = "chroma_db"):
    """
    Loads a document, splits it, and saves it to a vector store.
    """
    # 1. Load
    loader = TextLoader(file_path)
    documents = loader.load()
    
    # 2. Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    
    # 3. Create & Persist
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=persist_directory
    )
    return vectorstore

def initialize_vectorstore(data_dir: str = "data", persist_directory: str = "chroma_db"):
    """
    Scans a directory for text files and builds a vector store.
    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"📁 Created {data_dir}. Place project files there.")
        return None

    # Load all text files in the directory
    from langchain_community.document_loaders import DirectoryLoader
    loader = DirectoryLoader(data_dir, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print(f"⚠️ No documents found in {data_dir}.")
        return None

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    
    # Create & Persist
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=persist_directory
    )
    print(f"✅ Indexed {len(documents)} files into {persist_directory}.")
    return vectorstore

def load_vectorstore(persist_directory: str = "chroma_db"):
    """
    Loads an existing vector store from disk.
    """
    embeddings = get_embeddings()
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
