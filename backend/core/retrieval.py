import numpy as np
from core.vector_store import search

def retrieve(query_embedding, top_k=3):
    results = search(query_embedding, top_k = top_k)
    
    if not results:
        return None
    return results #list of dict








# from sklearn.metrics.pairwise import cosine_similarity


# SIMILARITY_THRESHOLD = 0.3

# def retrieve(query_embedding, df, top_k=3):
#     embeddings =  np.vstack(df["embedding"])
    
#     similarities = cosine_similarity(
#         embeddings,
#         np.array(query_embedding).reshape(1,-1)
#     ).flatten()
    
#     if similarities.max() < SIMILARITY_THRESHOLD:
#         return None
    
#     top_indices = similarities.argsort()[::-1][:top_k]
#     return df.iloc[top_indices]