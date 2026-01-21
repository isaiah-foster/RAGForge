import json
from .paths import SERVER_CONFIG_PATH, CLI_CONFIG_PATH

def create_default_server_config() -> dict:
    default_cfg = {
        "EMBEDDING_MODEL": "nomic-embed-text",
        "LANGUAGE_MODEL": "qwen3:latest",
        "INSTRUCTION_PROMPT": (
            "Determine if the following context is relevant to the user's question. If not, ignore it. If so, use the provided context to answer directly. Do not invent information. If context is missing or conflicting, say so. Keep responses concise and factual.\n\nContext:\n"
        ),
        "LOCAL_INFERENCE": True,
        "OLLAMA_API_KEY": "",
    }
    save_server_config(default_cfg)
    return default_cfg

def create_default_cli_config() -> dict:
    default_cfg = {
        "SERVER_ADDRESS": "127.0.0.1", 
    }
    save_cli_config(default_cfg)
    return default_cfg

def load_server_config() -> dict:
    if SERVER_CONFIG_PATH.exists():
        with open(SERVER_CONFIG_PATH) as f:
            return json.load(f)
    return create_default_server_config()

def load_cli_config() -> dict:
    if CLI_CONFIG_PATH.exists():
        with open(CLI_CONFIG_PATH) as f:
            return json.load(f)
    return create_default_cli_config()

def save_server_config(cfg: dict) -> None:
    with open(SERVER_CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
        
def save_cli_config(cfg: dict) -> None:
    with open(CLI_CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

# Load locally saved server URL - default to localhost if not set
def load_server_url() -> str:
    cfg = load_cli_config()
    return "http://"+cfg.get("SERVER_ADDRESS", "127.0.0.1") + ":8000"

def load_ollama_api_key():
    return load_server_config().get("OLLAMA_API_KEY", "")

def save_api_key(api_key: str) -> None:
    cfg = load_server_config()
    cfg["OLLAMA_API_KEY"] = api_key
    save_server_config(cfg)