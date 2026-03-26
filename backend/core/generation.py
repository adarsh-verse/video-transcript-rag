import requests

OLLAMA_GEN_URL = "http://localhost:11434/api/generate"

def generate_answer(query, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks["text"].tolist())

    prompt = f"""
You are a video course assistant.

Answer the user question using ONLY the transcript below.
Do NOT use outside knowledge.
Do NOT explain your reasoning.

If the answer is not present, reply exactly:
"I can only answer questions related to the video content."

TRANSCRIPT:
{context}

QUESTION:
{query}

Answer in 1-2 lines.
"""

    r = requests.post(
        OLLAMA_GEN_URL,
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return r.json()["response"]