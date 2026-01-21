import os
import chromadb
import ollama
from core.config import load_server_config
from core.paths import DATA_BASE_PATH, DATASET_PATH

# Class to load current embedding model's ChromaDB collection and add to/remove from it
class embedService:
    def __init__(self):
        self.model = load_server_config()["EMBEDDING_MODEL"]
        self.client = chromadb.PersistentClient(path=DATA_BASE_PATH) # identify chroma client in file system
        self.collection = self.client.get_or_create_collection(self.model) 
        self.dataset = [] #volatile storage for new data
        self.raw_chunks = []
        self.embedded_chunks = []
        
    # Load all .txt,.csv,.md files from the directory as a list of lines
    # ISSUE: store document names with a list of embedding models they've been vectorized to to track what to move
    def load_data(self): # make this load all files not currently in collection
        datasets_dir = DATASET_PATH

        if not os.path.isdir(datasets_dir):
            print(f"Datasets directory not found: {datasets_dir}")
            yield f"Datasets directory not found: {datasets_dir}\n"
            self.dataset = []
            return

        all_lines = []
        # load all text-like files in the Datasets directory
        for fname in sorted(os.listdir(datasets_dir)):
            fpath = os.path.join(datasets_dir, fname)
            if not os.path.isfile(fpath):
                continue
            # only load common text file extensions
            if not fname.lower().endswith((".txt", ".md", ".csv")):
                continue
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    # read non-empty stripped lines
                    lines = [line.rstrip("\n") for line in fh if line.strip()]
                    all_lines.extend(lines)
                    print(f"Loaded {len(lines)} entries from {fname}")
                    yield f"loaded {len(lines)} entries from {fname}\n"
            except Exception as e:
                print(f"Failed to read {fname}: {e}")
                yield f"failed to read {fname}: {e}\n"

        self.dataset = all_lines
        print(f"Total loaded {len(self.dataset)} entries from {datasets_dir}")
        yield f"Total loaded {len(self.dataset)} entries from {datasets_dir}\n"

    # Split text into sentences then embed, perform cosine similarity, and create chunks stored to self.raw_chunks
    def semantic_chunk(self, similarity_threshold=0.5, min_chunk_size=100, max_chunk_size=1000):
        """
        Perform semantic chunking on self.dataset using Ollama embeddings.
        
        Args:
            similarity_threshold: Cosine similarity threshold for splitting (0-1, lower = more splits)
            min_chunk_size: Minimum characters per chunk
            max_chunk_size: Maximum characters per chunk
        
        Returns:
            List of semantically coherent text chunks
        """
        if not self.dataset:
            print("No data loaded to chunk")
            yield "No data loaded to chunk\n"
            return []
        
        try:
            import requests
            import numpy as np
        except ImportError:
            print("Installing numpy...")
            yield "Installing numpy...\n"
            import subprocess
            subprocess.check_call(["pip", "install", "numpy"])
            import numpy as np
            import requests
        
        # Combine lines into sentences/paragraphs
        text = "\n".join(self.dataset)
        
        # Split into sentences
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return []
        
        print(f"Chunking {len(sentences)} sentences using Ollama embeddings...")
        yield f"Chunking {len(sentences)} sentences using Ollama embeddings...\n"
        
        # Get embeddings for all sentences
        try:
            print("Embedding sentences in batch...")
            yield "Embedding sentences in batch...\n"
            response = ollama.embed(
                model=self.model,
                input=sentences  # Can pass a list!
            )
            embeddings = [np.array(emb) for emb in response['embeddings']]
        except Exception as e:
            print(f"Error with batch embedding: {e}")
            yield f"Error with batch embedding: {e}\n"
            return []
            
        if len(embeddings) != len(sentences):
            print(f"Warning: Only got {len(embeddings)} embeddings for {len(sentences)} sentences")
            yield f"Warning: Only got {len(embeddings)} embeddings for {len(sentences)} sentences\n"
            # Filter sentences to match embeddings
            sentences = [s for i, s in enumerate(sentences) if i < len(embeddings)]
        
        # Calculate cosine similarity between consecutive sentences
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
        # Create chunks based on similarity
        chunks = []
        current_chunk = [sentences[0]]
        current_size = len(sentences[0])
        
        for i in range(1, len(sentences)):
            similarity = cosine_similarity(embeddings[i-1], embeddings[i])
            sentence_len = len(sentences[i])
            
            # Split if: similarity is low OR chunk would be too large
            should_split = (
                similarity < similarity_threshold or 
                current_size + sentence_len > max_chunk_size
            )
            
            # Don't split if chunk would be too small
            if should_split and current_size >= min_chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i]]
                current_size = sentence_len
            else:
                current_chunk.append(sentences[i])
                current_size += sentence_len
        
        # Add final chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        print(f"Created {len(chunks)} semantic chunks")
        print(f"Avg chunk size: {sum(len(c) for c in chunks) // len(chunks)} chars")
        yield f"Created {len(chunks)} semantic chunks\n"
        yield f"Avg chunk size: {sum(len(c) for c in chunks) // len(chunks)} chars\n"
        
        self.raw_chunks = chunks

    # Embed self.raw_chunks and store to self.embedded_chunks
    def embed_chunks(self):
        """Embed chunks using Ollama library (with batching!)"""
        import ollama
        
        print(f"Embedding {len(self.raw_chunks)} chunks for ChromaDB...")
        yield f"Embedding {len(self.raw_chunks)} chunks for ChromaDB...\n"
        
        try:
            response = ollama.embed(
                model=self.model,
                input=self.raw_chunks  # Batch all at once!
            )
            embeddings = response['embeddings']
            print(f"Successfully embedded {len(embeddings)} chunks")
            yield f"Successfully embedded {len(embeddings)} chunks\n"
            self.embedded_chunks = embeddings
        except Exception as e:
            print(f"Error embedding chunks: {e}")
            yield f"Error embedding chunks: {e}\n"
            self.embedded_chunks = []
    
    # Store sel.embedded_chunks to ChromaDB collection corresponding to self.model
    def store_data(self):
        for i in range(len(self.raw_chunks)):
            self.collection.add(
                ids= [f"id{i}"],
                embeddings=[self.embedded_chunks[i]],
                documents=[self.raw_chunks[i]],
                metadatas=[{"model": self.model}]
            )
        print("Data stored to ChromaDB")
        yield "Data stored to ChromaDB\n"

    # list all collections in the chroma client db
    def list_collections(self):
        collections = self.client.list_collections()
        print(collections)
        x = self.client.count_collections()
        print("Total collections:", x)
        yield f"{collections}\n"
        yield f"Total collections: {x}\n"
    
    # Remove a user chosen collection
    def remove_collection(self, name:str):
        self.client.delete_collection(name)
        print(f"Collection '{name}' removed.")
        yield f"Collection '{name}' removed.\n"


def embed_docs():
    service = embedService()
    yield from service.load_data()
    yield from service.semantic_chunk()
    yield from service.embed_chunks()
    yield from service.store_data()

def list_collections():
    service = embedService()
    yield from service.list_collections()

def remove_collection(name: str):
    service = embedService()
    yield from service.remove_collection(name)