from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.llm.groq_client import get_groq_client
from src.rag.vectorstore import load_vectorstore

def get_rag_chain(persist_directory: str = "chroma_db"):
    """
    Returns an LCEL RAG chain linked to the specified vector store.
    """
    llm = get_groq_client()
    vectorstore = load_vectorstore(persist_directory)
    retriever = vectorstore.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a research assistant. Answer questions using ONLY the provided context.\n\nContext:\n{context}"),
        ("user", "{question}")
    ])
    
    # The LCEL RAG Assembly Line
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain
