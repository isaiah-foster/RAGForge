# RAGForge

A flexible platform for **Retrieval-Augmented Generation (RAG)** that makes it easy to spin up local or server-hosted LLMs with retrieval pipelines.  
Use it through a **command-line interface (CLI)** for developers/ops for now

RAGForge helps individuals and organizations set up **chat interfaces powered by local models and custom knowledge bases**—without glue code.

---

## ✨ Features

- **Bring Your Own Model**  
  - Run locally with [Ollama](https://ollama.ai)

- **Retrieval Engine**  
  - Document ingestion (text, markdown, code for now)  
  - Chunking and embedding Chromadb
  - Vector storage with Chromadb

- **Chat Interfaces**  
  - **CLI:** quick terminal access for developers & operators  

---

## 🚀 Quickstart

### Prerequisites
- Ollama desktop
- Python 3.10+
- pull nomic-embed-text with ollama
```bash
ollama pull nomic-embed-text
```

### 1. Clone the repo
```bash
git clone https://github.com/your-username/ragforge.git
cd ragforge
```

### 2. Open a virtual environment and install packages
```bash
python -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -r requirements.txt
```

### 3. Run the program
- Set python interpreter to the one in your venv
- Start API
```bash
uvicorn apps.api.api:app --reload
```
- In a new terminal, run the cli
```bash
python apps/cli/cli.py
```
- Chat with the model!
Hint: ask about its context to see that its retrieved data from the cat_facts.txt file