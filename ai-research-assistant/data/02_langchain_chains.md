# Phase 2: LangChain Chains & Prompts

In Phase 1, we learned how to talk to the LLM directly. But in a real application, we don't want to hardcode every message. We need **Recipes**.

## 1. Prompt Templates
A `PromptTemplate` is like a fill-in-the-blank form. Instead of writing "Tell me about Dogs", we write "Tell me about {topic}". This allows our application to be dynamic.

## 2. LLMs and ChatModels
In LangChain, we distinguish between:
- **LLMs**: Traditional "text-in, text-out" models.
- **ChatModels**: Models designed for conversation (like those on Groq), which take a list of `BaseMessage` objects.

## 3. LCEL (LangChain Expression Language)
LangChain introduced a beautiful way to link components together using the pipe operator (`|`). 

Example:
```python
chain = prompt | model | parser
```
This means:
1.  Take the input.
2.  Pass it to the `prompt` template to get a formatted prompt.
3.  Pass that prompt to the `model` (LLM).
4.  Pass the model's response to the `parser` (to clean it up or turn it into JSON).

---

### Phase 2 Goal
We will build a simple "Research Query Chain". It will take a topic and output a structured research plan.
