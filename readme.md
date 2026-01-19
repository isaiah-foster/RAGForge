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
- Ollama
- Python >=3.12 & < 3.14
- pipx installed
- pull nomic-embed-text and qwen3:latest with ollama to start
```bash
ollama pull nomic-embed-text
ollama pull qwen3:latest
```

### 1. Install as a pipx package
```bash
pipx install git+https://github.com/isaiah-foster/RAGForge
```

### 2. Launch the API and run commands
- Start API
```bash
ragforge serve
```
- In a new terminal, run cli commands
- e.g. ```ragforge chat```
- Chat with the model!
Hint: ask about its context to see that its retrieved data from the cat_facts.txt file

### 3. Supported Commands
- type ```ragforge --help``` for a list of commands.

### 4. Notes
- To make config changes take effect in the same API instance, use ``ragforge serve --reload`` instead
- If on Arch linux and some other distros, you may have to run ``pip install tk tcl``
- If you don't want to use the default language and embedding models, run ``ragforge serve --reload``, and update your model configs before running ``ragforge chat``