import requests
from .main import app
from core.config import load_server_url

API_URL = load_server_url()

@app.command()
def chat():       
    """Start a chat"""
    print("Starting chat session with RagForge (type 'exit()' to quit)")
    print("-" * 50)
    
    while True:
        # Get user input
        query = input("> ")
        
        # Check if user wants to exit
        if query.lower() in ['exit()']:
            break
            
        # Send request to server
        try:
            resp = requests.post(f"{API_URL}/chat", json={"query": query},stream=True)
            if resp.status_code == 200:
                for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        print(chunk, end="", flush=True)
            else:
                print(f"Error {resp.status_code}: {resp.text}")
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
        
        print("\n" +"-" * 50)