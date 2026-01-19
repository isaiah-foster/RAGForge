import ollama
import chromadb
from core.config import load_config
from core.paths import DATA_BASE_PATH


#get model name
config = load_config()
    
EMBEDDING_MODEL = config["EMBEDDING_MODEL"]


def retrieve(query):
    embedded_query = ollama.embed(model = EMBEDDING_MODEL,input=query)["embeddings"][0]
    client = chromadb.PersistentClient(path=DATA_BASE_PATH) # identify chroma client in file system

    collection = client.get_or_create_collection(EMBEDDING_MODEL) 
    
    
    retrieved_array = collection.query(
        query_embeddings= embedded_query,
        n_results=5
    )["documents"][0]
         
    retrieved_string = "\n\n".join(retrieved_array)
    
    return retrieved_string
