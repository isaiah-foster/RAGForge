import os
import chromadb
import ollama
import json
import typer

app = typer.Typer(help="run", )

API_URL = "http://127.0.0.1:8000"
#get model name

class embedService:
    def __init__(self):
        with open("config.json", "r") as f:
            config = json.load(f)
        self.model = config["EMBEDDING_MODEL"]
        self.client = chromadb.PersistentClient(path="services/retrieval/Database/chroma_db") # identify chroma client in file system
        self.collection = self.client.get_or_create_collection("one") #ISSUE: figure out naming system,
        self.dataset = [] #volatile storage for new data
        
    #
    # ISSUE: Add cli feature to set embedding model.
    # allow option to migrate current vector DB over to new embedding type
    #
    # ISSUE: Allow removal of inactive collections based on embedding model name to save storage
    # store document names with a list of embedding models they've been vectorized to to track what to move
    #
    def load_data(self): # make this load all files not currently in collection
        base_dir = os.path.dirname(__file__)
        document_path = os.path.join(base_dir, "Datasets", "cat-facts.txt")

        with open(document_path, "r", encoding="utf-8") as file1:
            self.dataset = file1.readlines()
            print(f'Loaded {len(self.dataset)} entries')

    # embed each index of dataset, add to chroma collection with corresponding ID
    def embed(self):
        for i, chunk in enumerate(self.dataset): 
            embedded_chunk = ollama.embed(model=self.model, input=chunk)['embeddings'][0]
            self.collection.add(
                ids= [f"id{i}"],
                embeddings=[embedded_chunk],
                documents=[chunk.strip()],
                metadatas=[{"model": self.model}]
            )
            
            print(f"embedded chunk {i}/{len(self.dataset)} and added to collection")

@app.command()
def run():
    service = embedService()
    service.load_data()
    service.embed()