import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.llm.groq_client import get_groq_client
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    # 1. Initialize the Model
    llm = get_groq_client()

    # 2. Define the Prompt Template
    # We use placeholders like {topic} that will be filled in later.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional research assistant. Provide a concise 3-bullet point research plan for the given topic."),
        ("user", "Topic: {topic}")
    ])

    # 3. Create the Chain using LCEL (LangChain Expression Language)
    # The '|' operator pipes the output of one component into the next.
    # prompt -> formats the message
    # llm -> sends message to Groq
    # StrOutputParser -> extracts just the text from the response object
    chain = prompt | llm | StrOutputParser()

    # 4. Run the Chain
    topic = "The impact of quantum computing on cybersecurity"
    print(f"--- Researching topic: {topic} ---")
    
    response = chain.invoke({"topic": topic})

    # 5. Print the results
    print(response)

if __name__ == "__main__":
    main()
