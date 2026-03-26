from fastapi import FastAPI

from core.pipeline import process_video, answer_query

app = FastAPI()

global_df = None

@app.post("/process")
def process(input_source:str):
    global global_df
    global_df = process_video(input_source)
    return{"message": "Input processed successfully"}

@app.post("/ask")
def ask(query:str):
    if global_df is None:
        return {"error": "Process a video first"}
    
    result = answer_query(query, global_df)
    return result