import requests
import pandas as pd

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"

def create_embedding(text:str):
    r = requests.post(OLLAMA_EMBED_URL,
        json={
            "model": "bge-m3",
            "prompt": text
        }
    )
    return r.json()["embedding"]


def generate_embeddings(chunks):
    data = []
    for idx, chunk in enumerate(chunks):
        print(f"Embedding chunk {idx}")
        embedding = create_embedding(chunk["text"])
        
        data.append({
            "video_number": chunk["video_number"],
            "title": chunk["title"],
            "start": chunk["start"],
            "end": chunk["end"],
            "text": chunk["text"],
            "embedding": embedding
        })
        
    df = pd.DataFrame(data)
    return df