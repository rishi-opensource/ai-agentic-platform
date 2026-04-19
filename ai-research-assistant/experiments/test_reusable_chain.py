import sys
from pathlib import Path
# Tell Python to look in the root folder for our code
sys.path.append(str(Path(__file__).parent.parent))

from src.chains.qa_chain import get_research_chain, get_qa_chain

def main():
    # Notice we don't import ChatGroq or define prompts here!
    # All that complexity is hidden inside src/chains/qa_chain.py
    
    print("--- Test 1: Reusable Research Chain ---")
    research_chain = get_research_chain()
    print(research_chain.invoke({"topic": "Sustainable Energy"}))
    
    print("\n--- Test 2: Reusable QA Chain ---")
    qa_chain = get_qa_chain()
    print(qa_chain.invoke({"question": "Why is Groq so fast?"}))

if __name__ == "__main__":
    main()
