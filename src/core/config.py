import json
from .paths import CONFIG_PATH, API_PATH

def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}

def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

def load_api_key():
    with open(API_PATH, "r") as f:
        return f.readline().strip()