import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.llm.groq_client import get_groq_client
from langchain_core.messages import HumanMessage, SystemMessage

def main():
    # 1. Initialize the Model using our centralized factory
    llm = get_groq_client()

    # 3. Define the messages
    messages = [
        SystemMessage(content="You are a professional research assistant."),
        HumanMessage(content="Explain the advantage of using Groq for AI inference in one sentence."),
    ]

    print("--- Sending message to Groq ---")
    
    # 4. Invoke the model
    response = llm.invoke(messages)

    # 5. Print the results
    print(f"Response: {response.content}")

if __name__ == "__main__":
    main()
