import json
from .paths import CONFIG_PATH

def create_default_config() -> dict:
    default_cfg = {
        "EMBEDDING_MODEL": "nomic-embed-text",
        "LANGUAGE_MODEL": "qwen3:latest",
        "INSTRUCTION_PROMPT": (
            "Determine if the following context is relevant to the user's question. If not, ignore it. If so, use the provided context to answer directly. Do not invent information. If context is missing or conflicting, say so. Keep responses concise and factual.\n\nContext:\n"
        ),
        "LOCAL_INFERENCE": True,
        "OLLAMA_API_KEY": "",
    }
    save_config(default_cfg)
    return default_cfg

def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return create_default_config()

def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

def load_api_key():
    return load_config().get("OLLAMA_API_KEY", "")

def save_api_key(api_key: str) -> None:
    cfg = load_config()
    cfg["OLLAMA_API_KEY"] = api_key
    save_config(cfg)