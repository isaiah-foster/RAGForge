import typer
from . import chat, embed, upload, config

app = typer.Typer(help="RagForge CLI Help")

#register subcommand groups
app.add_typer(chat.app, name="chat")
app.add_typer(embed.app, name="embed")
app.add_typer(upload.app, name="upload-document")
app.add_typer(config.app, name="config")

if __name__ == "__main__":
    app()
    
    
# Available commands:
#python -m apps.cli.cli
#       chat start
#       embed run
#       upload-document  (placeholder for future subcommands)
#       config set-language-model
#       config set-embedding-model
#       config set-instruction-prompt