import chromadb
import ollama
import json

#get model name
with open("config.json", "r") as f:
    config = json.load(f)

EMBEDDING_MODEL = config["EMBEDDING_MODEL"]
#
# ISSUE: Add cli feature to set embedding model.
# allow option to migrate current vector DB over to new embedding type
#

dataset = [] #volatile storage for new data


client = chromadb.PersistentClient(path="apps/services/retrieval/Database/chroma_db") # identify chroma client in file system



collection_list = client.list_collections() 

    
collection = client.get_or_create_collection(EMBEDDING_MODEL) #create one collection per embedding model used

#
# ISSUE: Allow removal of inactive collections based on embedding model name to save storage
# store document names with a list of embedding models they've been vectorized to to track what to move
#

# read doc into a list of strings
with open('Datasets/cat-facts.txt', 'r') as file1:
    dataset = file1.readlines()
    print(f'Loaded {len(dataset)} entries')


# embed each index of dataset, add to chroma collection with corresponding ID
for i, chunk in enumerate(dataset): 
    embedded_chunk = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    collection.add(ids= f"id{i}", embeddings=embedded_chunk)
    print(f"embedded chunk {i}/{len(dataset)} and added to collection")


# test embeddings and make sure the database can be queried correctly
query = "Do cats have eyelashes"
embedded_query = ollama.embed(model = EMBEDDING_MODEL, input= query)['embeddings'][0]

results = collection.query(
    #query_texts=["example"] for chroma native embeddings
    query_embeddings=embedded_query,
    n_results=3 # how many results to return
)

print(results)