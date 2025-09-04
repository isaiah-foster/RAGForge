import ollama
import chromadb
import json

#get model name
with open("config.json", "r") as f:
    config = json.load(f)
    
EMBEDDING_MODEL = config["EMBEDDING_MODEL"]


query = "Hello world" # temp

embedded_query = ollama.embed(model = EMBEDDING_MODEL)
