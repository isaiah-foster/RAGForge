# cli option to configure Language Model, Embedding model
import typer
from core.config import load_server_config, save_server_config, load_cli_config, save_cli_config
from .main import server_app, app

#Commands to set configs on local machine. will not affect server unless server is local machine

@server_app.command()
def set_language_model(name: str):
    """
    Set language model from Ollama library.
    """
    cfg = load_server_config()
    cfg["LANGUAGE_MODEL"] = name
    save_server_config(cfg)
    typer.echo(f"Language model set to {name}. Make sure you have it pulled from Ollama")

@server_app.command()
def set_embedding_model(name: str):
    """
    Set embedding model from Ollama library.
    """
    cfg = load_server_config()
    cfg["EMBEDDING_MODEL"] = name
    save_server_config(cfg)
    typer.echo(f"Embedding model set to {name}. Make sure you have it pulled from Ollama")

@server_app.command()
def set_instruction_prompt(prompt: str):
    """
    (Advanced) Set the model's system prompt.
    """
    cfg = load_server_config()
    cfg["INSTRUCTION_PROMPT"] = prompt
    save_server_config(cfg)
    typer.echo("Prompt set.")

@server_app.command()
def list_configs():
    """
    List server configs
    """
    cfg = load_server_config()
    print(f"Embedding Model: {cfg["EMBEDDING_MODEL"]}\nLanguage Model: {cfg["LANGUAGE_MODEL"]}\nLocal Inference: {cfg["LOCAL_INFERENCE"]}")

@server_app.command()
def set_local_inference(enabled: bool):
    """
    Enable or disable local inference. (true/false)
    """
    cfg = load_server_config()
    cfg["LOCAL_INFERENCE"] = enabled
    save_server_config(cfg)
    status = "enabled" if enabled else "disabled"
    typer.echo(f"Local inference {status}.")

@server_app.command()
def set_ollama_api_key(api_key: str):
    """
    Set Ollama API key. Required for using cloud models.
    """
    from core.config import save_api_key
    save_api_key(api_key)
    typer.echo("Ollama API key set.")

@app.command()
def set_server_address(address: str):
    """
    Required for connecting to a remote RAGForge server (e.g. 127.0.0.1 for local).
    """
    cfg = load_cli_config()
    cfg["SERVER_ADDRESS"] = address
    save_cli_config(cfg)
    typer.echo(f"Server address set to {address}.")