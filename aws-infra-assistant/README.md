# 🚀 Multi-Agent AWS Infrastructure Assistant

A learning-focused project to build a multi-agent system for AWS infrastructure management using **Python**, **LangGraph**, and **LangChain**.

## 🧠 The Idea

The goal is to create a set of specialized agents, each an expert in a specific AWS domain (EC2, RDS, Lambda). A **Central Supervisor** routes user queries to the correct agent, allowing for modular and extensible infrastructure management through natural language.

## 🛠️ Current State: MVP

This project is currently in the **Minimum Viable Product (MVP)** stage.
- **Integration**: Uses the **AWS CLI** via Python's `subprocess` module.
- **Orchestration**: Powered by **LangGraph** using the Supervisor/Router pattern.
- **Memory**: Supports multi-turn conversations through session-based state persistence.

> [!IMPORTANT]
> This is a learning project designed for clarity and modularity. In the current MVP, AWS CLI credentials are read from `~/.aws/credentials`.

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
