import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# 1. Load Environment Variables
# This reads the .env file so we can access our GOOGLE_API_KEY
load_dotenv()

def main():
    # 2. Initialize the Model
    # We try 'gemini-3-flash-preview' as found in the available models list.
    # We set temperature=0.0 for deterministic results.
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0.0,
    )

    # 3. Define the messages
    # SystemMessage: Defines the AI's identity.
    # HumanMessage: The user's input.
    messages = [
        SystemMessage(content="You are a professional research assistant."),
        HumanMessage(content="Explain what an AI Agent is in one sentence."),
    ]

    print("--- Sending message to Gemini ---")
    
    # 4. Invoke the model
    # .invoke() sends the messages and waits for the full response.
    response = llm.invoke(messages)

    # 5. Print the results
    print(f"Response: {response.content}")

if __name__ == "__main__":
    main()
