import typer

app = typer.Typer(help="RagForge CLI Help")
server_app = typer.Typer(help="RAGForge Server Commands")
app.add_typer(server_app, name="server", help="server --help for server commands")

from . import chat, configs, database, serve, upload


if __name__ == "__main__":
    app()