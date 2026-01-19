import typer

app = typer.Typer(help="RagForge CLI Help")

from . import chat, config_cmds, upload, embed, serve

if __name__ == "__main__":
    app()