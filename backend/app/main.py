from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional

from core.pipeline import process_video, answer_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global_df = None

@app.post("/process")
async def process(file: Optional[UploadFile] = File(None),input_source: Optional[str] = Form(None)):
    global global_df
    if file:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        global_df = process_video(file_path)
    elif input_source:
        global_df = process_video(input_source)
    else:
        return{"error":"No Input Provided"}
    
    
    return{"message": "Input processed successfully"}

@app.post("/ask")
def ask(query:str):
    if global_df is None:
        return {"error": "Process a video first"}
    
    result = answer_query(query, global_df)
    return result