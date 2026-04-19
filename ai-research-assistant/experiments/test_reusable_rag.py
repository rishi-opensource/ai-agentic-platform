import sys
from pathlib import Path

# Path helper
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.vectorstore import create_vectorstore, load_vectorstore
from src.rag.retrieval_chain import get_rag_chain

import shutil

def main():
    # 1. Setup the Knowledge Base
    # CLEANUP: Remove old database to avoid duplicate chunks
    persist_dir = "chroma_db"
    if Path(persist_dir).exists():
        shutil.rmtree(persist_dir)
        print(f"--- Cleared old database at {persist_dir} ---")

    print("--- Polishing the Knowledge Base ---")
    create_vectorstore("data/research_notes.txt", persist_directory=persist_dir)
    
    # 2. Get the RAG Chain
    # Notice: ZERO prompt engineering or model setup needed here!
    print("--- Initializing Reusable RAG Chain ---")
    rag_chain = get_rag_chain()
    
    # 3. Ask a question
    query = "How do we access the central reactor in Project Antigravity?"
    print(f"\nQuestion: {query}")
    
    # DEBUG: See what the retriever finds
    retriever = load_vectorstore().as_retriever()
    docs = retriever.invoke(query)
    print("--- Debug: Retrieved Chunks ---")
    for doc in docs:
        print(f"- {doc.page_content[:100]}...")
    
    response = rag_chain.invoke(query)
    print(f"\nAnswer: {response}")

if __name__ == "__main__":
    main()
