import pandas as pd
import numpy as np
from embedding_utils import create_embedding
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import requests



df = joblib.load('embeddings.joblib')


incoming_query = input("Ask a Question: ")
question_embedding = create_embedding(incoming_query)


def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2",
    "prompt": prompt,
    "stream":False
   })
    response = r.json()
    return response
    

similarities = cosine_similarity(
    np.vstack(df['embedding']),
    np.array(question_embedding).reshape(1,-1)).flatten()

SIMILARITY_THRESHOLD = 0.3
if similarities.max() < SIMILARITY_THRESHOLD:
    print("I can only answer questions related to the video content.")
    exit()
    
top_results = 1
# best_chunk_indices = similarities.argsort()[::-1][:top_results]
best_idx = similarities.argmax()
best_row = df.iloc[best_idx]



video_title = best_row["title"]
video_number = best_row["video_number"]
start_time = best_row["start"]
end_time = best_row["end"]
chunk_text = best_row["text"][:500]

prompt = f"""
You are a video course assistant.

Answer the user question using ONLY the transcript below.
Do NOT use outside knowledge.
Do NOT explain your reasoning.
Do NOT mention sources.

If the answer is not present in the transcript, reply exactly:
"I can only answer questions related to the video content."

TRANSCRIPT:
{chunk_text}

QUESTION:
"{incoming_query}"

TASK:
Write a concise 1–2 line explanation.
"""

with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

response = inference(prompt)
final_answer = f"""
Video Title: {video_title}
Video Number: {video_number}
Timestamp: {start_time}s – {end_time}s
Explanation: {response['response']}
"""

print(final_answer)


with open("response.txt", "w", encoding="utf-8") as f:
    f.write(final_answer)