# cli option to configure Language Model, Embedding model
import typer
from core.config import load_config, save_config
from .cli import app

@app.command()
def set_language_model(name: str):
    """
    Set the language model name in config.
    """
    cfg = load_config()
    cfg["LANGUAGE_MODEL"] = name
    save_config(cfg)
    typer.echo(f"Language model set to {name}. Make sure you have it pulled from Ollama")

@app.command()
def set_embedding_model(name: str):
    """
    Set the embedding model name in config.
    """
    cfg = load_config()
    cfg["EMBEDDING_MODEL"] = name
    save_config(cfg)
    typer.echo(f"Embedding model set to {name}. Make sure you have it pulled from Ollama")

@app.command()
def set_instruction_prompt(prompt: str):
    """
    (Advanced) Set the model's system RAG prompt in config.
    """
    cfg = load_config()
    cfg["INSTRUCTION_PROMPT"] = prompt
    save_config(cfg)
    typer.echo("Prompt set.")
    
@app.command()
def list_configs():
    """List current configs
    """
    cfg = load_config()
    print(f"Embedding Model: {cfg["EMBEDDING_MODEL"]}\nLanguage Model: {cfg["LANGUAGE_MODEL"]}\nLocal Inference: {cfg["LOCAL_INFERENCE"]}")