import sys
import os
from pathlib import Path

# Path helper for our imports
sys.path.append(str(Path(__file__).parent.parent))

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.llm.groq_client import get_groq_client

def main():
    # 1. Load the "Secret" Document
    print("--- Loading Document ---")
    file_path = "data/research_notes.txt"
    loader = TextLoader(file_path)
    documents = loader.load()

    # 2. Split into Chunks
    print("--- Splitting into Chunks ---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    # 3. Create Embeddings
    print("--- Creating Embeddings (this might take a few seconds) ---")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Store in Vector Database (ChromaDB)
    print("--- Initializing Vector Store ---")
    persist_directory = "chroma_db"
    # We use ephemeral vector store for the experiment, or persist it
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=persist_directory
    )

    # 5. Build our RAG Chain using LCEL
    llm = get_groq_client()
    
    # We define a prompt that explicitly uses the context
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a research assistant. Answer the question using ONLY the provided context. If you don't know, say you don't know.\n\nContext:\n{context}"),
        ("user", "{question}")
    ])

    # This is the RAG Chain:
    # 1. Takes the user question
    # 2. Retrieves context from VectorStore
    # 3. Formats the prompt
    # 4. Sends to LLM
    # 5. Parses output to string
    rag_chain = (
        {"context": vectorstore.as_retriever(), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 6. Ask the Secret Questions
    questions = [
        "What is the lead scientist's name?",
        "What is the key advantage of Temporal Flux Capacitors?",
        "What isotope exhibits antigravity properties?"
    ]

    for query in questions:
        print(f"\nQuestion: {query}")
        response = rag_chain.invoke(query)
        print(f"Answer: {response}")


if __name__ == "__main__":
    main()
