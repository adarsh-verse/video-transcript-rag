import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

SIMILARITY_THRESHOLD = 0.3

def retrieve(query_embedding, df, top_k=3):
    embeddings =  np.vstack(df["embedding"])
    
    similarities = cosine_similarity(
        embeddings,
        np.array(query_embedding).reshape(1,-1)
    ).flatten()
    
    if similarities.max() < SIMILARITY_THRESHOLD:
        return None
    
    top_indices = similarities.argsort()[::-1][:top_k]
    return df.iloc[top_indices]