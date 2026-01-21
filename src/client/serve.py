import typer
import uvicorn
from core.paths import ensure_dirs
from .main import server_app
from core.config import load_server_config

#serve command to launch local server for LLM inference API

@server_app.command()
def start(
    
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(8000, "--port"),
    reload: bool = typer.Option(False, "--reload/--no-reload"),
    lan: bool = typer.Option(False, "--lan/--no-lan"),
):
    """
    Launch LLM inference API
    """
    ensure_dirs()  # Ensure necessary directories exist
    load_server_config()  # Ensure config is loaded at startup

    if lan:
        uvicorn.run(
        "api.api:app",
        host = "0.0.0.0",
        port = port,
        reload = reload,
    )
    else:
        uvicorn.run(
            "api.api:app",
            host=host,
            port=port,
            reload=reload,
    )
