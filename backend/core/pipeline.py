from core.ingestion import transcribe_audio
from core.chunking import merge_chunks
from core.embedding import generate_embeddings, create_embedding
from core.retrieval import retrieve
from core.generation import generate_answer
from core.input_handler import handle_input
from core.vector_store import add_embeddings, save_index
import os

def process_video(input_source, video_number = 1):
    audio_path = handle_input(input_source)
    data = transcribe_audio(audio_path, video_number)
    merged_chunks = merge_chunks(data["chunks"])
    df = generate_embeddings(merged_chunks)
    embeddings = df["embedding"].tolist()
    metadata = []
    for _, row in df.iterrows():
        metadata.append({
            "text": row["text"],
            "title": row["title"],
            "start": row["start"],
            "end": row["end"]
        })
    add_embeddings(embeddings, metadata)
    if audio_path.startswith("temp") and os.path.exists(audio_path):
        os.remove(audio_path)
    save_index()

def answer_query(query, df):
    query_embedding = create_embedding(query)
    
    retrieved = retrieve(query_embedding)
    
    if not retrieved:
        return "I can only answer questions related to the video content."
    context = " ".join(item["text"] for item in retrieved)
    answer = generate_answer(query, context)
    top_row = retrieved[0]
    return {
        "video_title": top_row["title"],
        "timestamp": f"{top_row["start"]}s - {top_row["end"]}s",
        "answer": answer
    }
   
def answer_query(query):
    query_embedding = create_embedding(query)
    retrieved = retrieve(query_embedding)
    if not retrieved:
        return "I can only answer questions related to the video content."
    context = " ".join(item["text"] for item in retrieved)
    answer = generate_answer(query, context)
    top_row = retrieved[0]
    return {
        "video_title": top_row["title"],
        "timestamp": f"{top_row["start"]}s - {top_row["end"]}s",
        "answer": answer
    }