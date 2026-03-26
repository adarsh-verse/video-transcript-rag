from core.ingestion import transcribe_audio
from core.chunking import merge_chunks
from core.embedding import generate_embeddings, create_embedding
from core.retrieval import retrieve
from core.generation import generate_answer
from core.input_handler import handle_input

def process_video(input_source, video_number = 1):
    audio_path = handle_input(input_source)
    data = transcribe_audio(audio_path, video_number)
    merged_chunks = merge_chunks(data["chunks"])
    df = generate_embeddings(merged_chunks)
    return df

def answer_query(query, df):
    query_embedding = create_embedding(query)
    
    retrieved = retrieve(query_embedding, df)
    
    if retrieved is None:
        return "I can only answer questions related to the video content."
    
    answer = generate_answer(query, retrieved)
    
    top_row = retrieved.iloc[0]
    
    return {
        "video_title": top_row["title"],
        "timestamp": f"{top_row["start"]}s - {top_row["end"]}s",
        "answer": answer
    }