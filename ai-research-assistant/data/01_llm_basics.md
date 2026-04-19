# Phase 1: LLM Basics (The Foundation)

Welcome to the first phase! Before we dive into the complexity of agents, we must understand the "intelligence" that powers them.

## 1. What is an LLM?
Large Language Models (LLMs) are statistical models trained on massive amounts of text. They don't "think" like humans; instead, they are incredibly sophisticated at predicting the next most likely word (or "token") in a sequence.

## 2. The Anatomy of a Prompt
When we talk to an LLM like **Groq** (using Llama models), we typically use two types of messages:
- **System Message**: This sets the "persona" or boundaries for the LLM. (e.g., "You are a helpful research assistant.")
- **User Message**: The actual query or instruction.

## 3. Key Hyperparameters
- **Temperature**: Controls randomness. 
    - `0.0` = Deterministic (best for facts/code).
    - `1.0`+ = Creative (best for brainstorming).
- **Max Output Tokens**: Limits the length of the response.
- **Stop Sequences**: Tells the model where to stop generating.

## 4. What are Tokens?
LLMs don't see words; they see "tokens" (chunks of characters). For example, "learning" might be one token, while a rarer word might be split into three. 

---

### Phase 1 Goal
We will build a simple script that sends a message to **Groq** and prints the response. This helps us ensure our API key and network connection are working.
