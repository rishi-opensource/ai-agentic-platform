from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.llm.groq_client import get_groq_client

def get_research_chain():
    """
    Returns a chain that generates a research plan for a given topic.
    """
    llm = get_groq_client()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional research assistant. Provide a structured research plan for the given topic."),
        ("user", "Topic: {topic}")
    ])
    
    # We return the chain itself
    return prompt | llm | StrOutputParser()

def get_qa_chain():
    """
    Returns a simple question-answering chain.
    """
    llm = get_groq_client()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful research assistant. Answer the user's question clearly and concisely."),
        ("user", "{question}")
    ])
    
    return prompt | llm | StrOutputParser()
