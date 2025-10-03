# cli option to configure Language Model, Embedding model, context window, chunking method, retrieval size, collection

# cli option to configure Language Model, Embedding model, context window, chunking method, retrieval size, collection

import typer
import json
from pathlib import Path

app = typer.Typer()

_CONFIG_PATH = Path(__file__).parent.parent.parent / "config.json"

def _load_config():
    if _CONFIG_PATH.exists():
        with open(_CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def _save_config(cfg):
    with open(_CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

@app.command()
def set_language_model(name: str):
    """
    Set the language model name in config.
    """
    cfg = _load_config()
    cfg["LANGUAGE_MODEL"] = name
    _save_config(cfg)
    typer.echo(f"Set LANGUAGE_MODEL to {name}")

@app.command()
def set_embedding_model(name: str):
    """
    Set the embedding model name in config.
    """
    cfg = _load_config()
    cfg["EMBEDDING_MODEL"] = name
    _save_config(cfg)
    typer.echo(f"Set EMBEDDING_MODEL to {name}")

@app.command()
def set_instruction_prompt(prompt: str):
    """
    Set the instruction prompt in config.
    """
    cfg = _load_config()
    cfg["INSTRUCTION_PROMPT"] = prompt
    _save_config(cfg)
    typer.echo("Set INSTRUCTION_PROMPT.")