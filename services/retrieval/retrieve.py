import ollama
import chromadb
import json


#get model name
with open("config.json", "r") as f:
    config = json.load(f)
    
EMBEDDING_MODEL = config["EMBEDDING_MODEL"]


def retrieve(query):
    embedded_query = ollama.embed(model = EMBEDDING_MODEL,input=query)["embeddings"][0]
    client = chromadb.PersistentClient(path="services/retrieval/Database/chroma_db") # identify chroma client in file system
    
    collection = client.get_collection("one") #FIX NAME of collection
    
    
    retrieved_array = collection.query(
        query_embeddings= embedded_query,
        n_results=5
    )["documents"][0]
         
    retrieved_string = "\n\n".join(retrieved_array)
    
    return retrieved_string
