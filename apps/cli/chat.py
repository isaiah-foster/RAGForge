import typer
import requests

app = typer.Typer(help="Chat with the API")

API_URL = "http://127.0.0.1:8000"

@app.command()
def start():       
    """Start a chat session with the server."""
    print("Starting chat session with RagForge(type 'exit' to quit)")
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