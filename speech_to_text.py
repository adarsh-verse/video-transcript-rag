import whisper
import json
import time
import os

# Add ffmpeg to PATH (Windows-only)
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"


AUDIO_DIR = "audios"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

start_time = time.time()

model = whisper.load_model("small", device="cpu")

video_number = 1

for filename in os.listdir(AUDIO_DIR):
    if not filename.lower().endswith(".mp3"):
        continue
    
    
    audio_path = os.path.join(AUDIO_DIR,filename)
    
    title = os.path.splitext(filename)[0]
    
    print(f"\n Processing: {title}")
    
    result = model.transcribe(
        audio_path,
        fp16=False,
        # language="hi"
        # task="translate"
        verbose=False   
    )
    
    chunks = []
    full_text = ""
    
    for segment in result["segments"]:
        text = segment["text"].strip()
        if text:
            chunks.append({
                "video_number": video_number,
                "title":title,
                "start": round(segment["start"],2),
                "end": round(segment["end"],2),
                "text": text  
            })
            
            full_text += text + " "
    
    final_json = {
        "chunks":chunks,
        "full_text":full_text.strip()
        
    }
    
    output_file = os.path.join(
        OUTPUT_DIR,
        f"{video_number:02d}_{title}.json"
    )
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)

    print(f"Saved: {output_file}")

    video_number += 1
    
end_time = time.time()
print(f"\n Total time taken: {end_time - start_time} seconds")
   


