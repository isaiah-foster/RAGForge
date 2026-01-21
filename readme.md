# RAGForge

A flexible platform for businesses to configure their own local **Retrieval-Augmented Generation (RAG)**.

RAGForge lets individuals and organizations quickly spin up **chat interfaces powered by local models and custom knowledge bases** in just a few commands with no glue code.

---

## Features

- **Server and client features bundled in one**
  - Configure as a server with ``ragforge server`` command subgroup.
  - Configure as an end user with base command group.
  - Configure as both if you want to keep it local!

- **Customization**
  - Run your server visible to **localhost**(default) or to **LAN** for businesses
  - Download **any Ollama compatible models** for inference and embedding.
  - **Upload** documents from client to server and embed for retrieval
  - Set your own **system prompt** to help the model understand context (there is a default prompt).
  - Switch between server-local inference (default) and ollama cloud inference.
    -  Cloud: Set your ollama api key in server config. Retrieved documents will be sent to the cloud. Local is recommended for maximum privacy.
  - ChromaDB collections are made per embedding model, and can be deleted via server CLI.

- **Chat Interfaces**  
  - **CLI:** terminal REPL with streamed responses
  - **GUI:** coming soon...
 
- **Retrieval Engine**
  - Document ingestion (text, markdown, csv, code, PDFs)  
  - Semantic data chunking via cosine similarity
  - Vector storage with Chromadb
  - user configured context retrieval size

---

## Quickstart

### Prerequisites
- Ollama/Ollama Desktop (Windows)
- Python >=3.12 & < 3.14

### 1. Install as a pip package and configure
```bash
pip install git+https://github.com/isaiah-foster/RAGForge
```
- Set server configs to use models you have pulled. Defauts are nomic-embed-text and qwen3:latest.
```bash
ollama pull nomic-embed-text # embedding
ollama pull qwen3:latest # inference
```

### 2. Launch the API and run commands
- Start API on localhost:
  ```bash
  ragforge server start
  ```
  - In a new terminal, run cli commands e.g. ``ragforge chat``
- Start API on LAN for exposure to your network.
  ```bash
  ragforge server serve --lan
  ```
  - Note: you may have to configure network settings to securely accept traffic on port 8000 (iptables etc.).
  - From any device on the network, run
    ```bash
    ragforge set-server-address <your server IP address>
    ragforge chat
    ```

### 3. Supported Commands
- ```ragforge --help``` for a list of client commands.
- ```ragforge server --help``` for a list of server commands.
