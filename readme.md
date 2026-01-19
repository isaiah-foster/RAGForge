# RAGForge

A flexible platform for **Retrieval-Augmented Generation (RAG)** that makes it easy to spin up local or server-hosted LLMs with retrieval pipelines.  
Use it through a **command-line interface (CLI)** for developers/ops for now

RAGForge helps individuals and organizations set up **chat interfaces powered by local models and custom knowledge bases**—without glue code.

---

## Features

- **Bring Your Own Model**  
  - Run locally with [Ollama](https://ollama.ai)

- **Retrieval Engine**
  - Document ingestion (text, markdown, code for now)  
  - Chunking and embedding Chromadb
  - Vector storage with Chromadb

- **Chat Interfaces**  
  - **CLI:** quick terminal access for developers & operators  

---

## Quickstart

### Prerequisites
- Ollama desktop
- Python 3.10+
- pull nomic-embed-text with ollama
- install tk and tcl (```sudo pacman -S tk tcl``` if on arch)
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
- Set python interpreter to the one in your venv

### 3. Install ragforge as a pip package in you venv
```bash
pip install -e .
```

### 4. Launch the API and run commands
- Start API
```bash
ragforge serve
```
- In a new terminal, run cli commands
- e.g. ```ragforge chat```
- Chat with the model!
Hint: ask about its context to see that its retrieved data from the cat_facts.txt file

### 5. Supported Commands
- type ```ragforge --help``` for a list of commands.