import whisper
import os
import time

# Add ffmpeg to PATH (Windows-only)
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"


start_time = time.time()

model = whisper.load_model("small", device="cpu")

def transcribe_audio(audio_path:str, video_number:int):
    result = model.transcribe(
        audio_path,
        fp16=False,
        verbose=False
    )
    chunks = []
    full_text = ""
    
    for segment in result["segments"]:
        text = segment["text"].strip()
        if text:
            chunk = {
                "video_number": video_number,
                "title":audio_path.split("/")[-1].split(".")[0],
                "start": round(segment["start"],2),
                "end": round(segment["end"],2),
                "text": text  
            }
            chunks.append(chunk)
            full_text += text + " "
    return{
        "chunks":chunks,
        "full_text": full_text.strip()
    }
    
end_time = time.time()
print(f"\n Total time taken: {end_time - start_time} seconds")
   


