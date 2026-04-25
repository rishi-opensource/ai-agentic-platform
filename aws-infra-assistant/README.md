# 🚀 Multi-Agent AWS Infrastructure Assistant

A learning-focused project to build a multi-agent system for AWS infrastructure management using **Python**, **LangGraph**, and **LangChain**.

## 🧠 The Idea

The system is a **True Multi-Agent System** that uses a **Plan-and-Execute** pattern. It consists of specialized domain experts (EC2, RDS, Lambda) coordinated by a strategic Supervisor.

## 🛠️ Current State: Evolved System

The assistant has evolved beyond simple routing into a robust orchestration framework:
- **Planning Supervisor**: Analyzes complex queries and generates execution plans involving multiple agents.
- **Specialized Agents**: Each agent has its own **System Prompt** and domain-specific expertise.
- **Reasoning Loops**: Agents receive tool outputs directly, reasoning over them to decide if further action is required.
- **Execution Tracing**: Real-time visibility into the system's "thinking" process via a step-by-step trace in the CLI.
- **Resilient Execution**: AWS CLI communication includes mandatory timeouts and automatic retries.

## 📂 Project Structure

- `agents/`: Domain-specific agents (EC2, RDS, Lambda).
- `tools/`: Core utilities including the AWS CLI wrapper.
- `orchestrator.py`: LangGraph graph definitions and Supervisor logic.
- `main.py`: Interactive CLI entry point.

## 🚀 Future Roadmap

### Boto3 Migration
We will migrate from the CLI subprocess wrapper to **boto3** (the official AWS SDK for Python). This will provide:
- Better performance and error handling.
- Native Python support for all AWS features.
- Structured API responses without CLI parsing.

### Human-in-the-loop (HITL)
Integrate LangGraph's HITL capabilities to require user approval before performing destructive actions (like deleting an instance).

### Web Dashboard
Move from a CLI to a modern Web UI for better visualization of resources and agent thoughts.

## ⚙️ Setup

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Set API Key**: `export OPENAI_API_KEY='your-key'`
3. **Run**: `python main.py`
