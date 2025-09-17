import typer
import requests
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parents[2]  # adjust as needed
CONFIG_PATH = ROOT_DIR / "config.json"

#get config
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

LANGUAGE_MODEL = config["LANGUAGE_MODEL"]

app = typer.Typer()

API_URL = "http://127.0.0.1:8000"

@app.command()
def chat():
    """Start a chat session with the server."""
    print(f"Starting chat session with {LANGUAGE_MODEL}(type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        # Get user input
        query = input("> ")
        
        # Check if user wants to exit
        if query.lower() in ['exit']:
            break
            
        # Send request to server
        try:
            resp = requests.post(f"{API_URL}/chat", json={"query": query})
            if resp.status_code == 200:
                print(resp.json()["response"])
            else:
                print(f"Error {resp.status_code}: {resp.text}")
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    app()