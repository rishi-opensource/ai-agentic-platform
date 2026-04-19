import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_groq_client(model_name: str = "llama-3.3-70b-versatile", temperature: float = 0):
    """
    Creates and returns a ChatGroq client.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    
    return ChatGroq(
        model_name=model_name,
        temperature=temperature,
        groq_api_key=api_key
    )
