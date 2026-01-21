import requests
import typer
from .main import app, server_app
from core.config import load_server_url
from server.embedding import embedService

API_URL = load_server_url()
        
@app.command()
def embed_docs():
    """
    Embed all documents in server queue to ChromaDB
    """
    try:
        resp = requests.post(f"{API_URL}/embed", stream=True)
        if resp.status_code == 200:
            for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    print(chunk, end="", flush=True)
        else:
            print(f"Error {resp.status_code}: {resp.text}")
    except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            

@app.command()
def list_collections():
    """
    List all ChromaDB collections
    """
    try:
        resp = requests.post(f"{API_URL}/list_collections", stream=True)
        if resp.status_code == 200:
            for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    print(chunk, end="", flush=True)
        else:
            print(f"Error {resp.status_code}: {resp.text}")
    except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
    
@server_app.command()
def remove_collection(name: str):
    """
    Remove a chosen ChromaDB Collection based on embedding model from local machine (not server)
    """
    service = embedService()
    service.remove_collection(name)
    typer.echo(f"ChromaDB collection {name} removed.")