# apps/cli/serve.py
import typer
import uvicorn
from .cli import app
from core.config import load_config

@app.command()
def serve(
    
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(8000, "--port"),
    reload: bool = typer.Option(False, "--reload/--no-reload"),
):
    """
    Launch LLM inference API
    """
    load_config()  # Ensure config is loaded at startup
    uvicorn.run(
        "apps.api.api:app",
        host=host,
        port=port,
        reload=reload,
    )
