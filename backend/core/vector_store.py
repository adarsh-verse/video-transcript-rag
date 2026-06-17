import faiss
import numpy as np
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

INDEX_FILE = os.path.join(DATA_DIR, "faiss_index.bin")
METADATA_FILE = os.path.join(DATA_DIR, "metadata.pkl")

index = None

metadata_store = []

def create_index(dimension: int):
    global index
    index = faiss.IndexFlatL2(dimension)


def add_embeddings(embeddings, metadata):
    global index, metadata_store

    vectors = np.array(embeddings).astype("float32")

    if index is None:
        create_index(vectors.shape[1])

    index.add(vectors)
    metadata_store.extend(metadata)


def search(query_vector, top_k=3,threshold =1.5):
    global index, metadata_store

    query_vector = np.array([query_vector]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []
    for i , idx in enumerate(indices[0]):
        if idx < len(metadata_store):
            if distances[0][i] < threshold:
                results.append(metadata_store[idx])
    return results
        

def save_index():
    global index, metadata_store
    print("Saving FAISS index...")
    if index is not None:
        faiss.write_index(index, INDEX_FILE)
        
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(metadata_store,f)
    print("Saving FAISS index...")
        
def load_index():
    global index, metadata_store
    
    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)
    
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "rb") as f:
            metadata_store = pickle.load(f)
        
        