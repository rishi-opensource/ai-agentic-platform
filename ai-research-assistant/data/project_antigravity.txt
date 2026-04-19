# Phase 3: RAG (Retrieval Augmented Generation)

While LLMs are smart, they don't know your specific business data, secret research, or what you ate for breakfast. **RAG** solves this by letting the LLM "read" your documents before it answers.

## 1. The RAG Workflow
Think of RAG like an **Open-Book Exam**:
1.  **Retrieval**: The assistant looks through your documents to find relevant chapters.
2.  **Augmentation**: It adds those chapters to its prompt as context.
3.  **Generation**: It answers the question using both its internal knowledge and the provided context.

## 2. Chunking & Overlap
We can't feed a 100-page PDF into an LLM all at once (it's too much data/tokens). Instead, we split it:
- **Chunks**: Small snippets of text (e.g., 500 characters).
- **Overlap**: We repeat the last few words of Chunk 1 at the start of Chunk 2. This prevents a sentence from being "cut in half" and losing its meaning.

## 3. Embeddings (The "Matchmaker")
How does the computer find "relevant" text? 
- We turn text into **Vectors** (lists of numbers).
- Similar meanings = similar numbers.
- Example: "King" and "Queen" will have very similar vector numbers.

## 4. Vector Store (The Database)
A traditional database (like Excel) looks for exact words. A **Vector Store** (like ChromaDB) looks for **meanings**. It stores all our "chunks" as numbers so we can find them instantly using a search query.

---

### Phase 3 Goal
We will:
1. Create a `research_notes.txt` file.
2. Build a script to **Embed** and store those notes in ChromaDB.
3. Ask the LLM a question that *only* those notes can answer!
