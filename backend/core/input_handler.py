import os
import yt_dlp
import subprocess
import logging
import uuid 
import shutil
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "audios")
os.makedirs(AUDIO_DIR, exist_ok=True)

def is_url(input_source:str):
    try:
        result = urlparse(input_source)
        return result.scheme in ["http", "https"] and result.netloc !=""
    except:
        return False

def generate_unique_filename(base_name: str):
    unique_id = str(uuid.uuid4())[:8]
    return f"{unique_id}_{base_name}"
    
    

def download_audio_from_url(url: str):
    logging.info("Detected URL input...")
    output_path = os.path.join(AUDIO_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
        "noplaylist": True,
        # "cookiesfrombrowser": ("chrome",),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        audio_path = convert_video_to_audio(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        return audio_path
    except Exception as e:
        raise Exception(f"Unable to download video.Please upload the file manually, {str(e)}")
        
            

def convert_video_to_audio(video_path: str):
    logging.info("Converting video to audio...")
    base_name = os.path.basename(os.path.splitext(video_path)[0])
    base_name = generate_unique_filename(base_name)
    audio_path = os.path.join(AUDIO_DIR, base_name + ".mp3")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-ab", "192k",
        "-ar", "44100",
        "-y",
        audio_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"FFmpeg failed: {result.stderr}")
    return audio_path

def move_audio_to_directory(audio_path: str):
    logging.info("Processing local audio...")
    base_name = os.path.basename(audio_path)
    base_name = generate_unique_filename(os.path.splitext(base_name)[0])
    ext = os.path.splitext(audio_path)[1]
    new_path = os.path.join(AUDIO_DIR, base_name + ext)
    
    shutil.move(audio_path, new_path)
    return new_path


    

def handle_input(input_source: str):
    
    input_lower = input_source.lower()
    
    if is_url(input_source):
        return download_audio_from_url(input_source)
    
    if input_lower.endswith((".mp3", ".wav")):
        logging.info("Detected local audio...")
        return move_audio_to_directory(input_source)
    
    if input_lower.endswith((".mp4", ".mkv", ".avi", ".mov", ".webm")):
        logging.info("Detected local video..")
        return convert_video_to_audio(input_source)
    
    raise ValueError("Unsupported input format")