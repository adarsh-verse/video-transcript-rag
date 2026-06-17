from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from core.vector_store import load_index
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
# load_index()

# global_df = None

@app.post("/process")
async def process(file: Optional[UploadFile] = File(None),input_source: Optional[str] = Form(None)):
    # global global_df
    if file:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        process_video(file_path)
    elif input_source:
        process_video(input_source)
    else:
        return{"error":"No Input Provided"}
    
    
    return{"message": "Input processed successfully"}

@app.post("/ask")
def ask(query:str):
    result = answer_query(query)
    return result