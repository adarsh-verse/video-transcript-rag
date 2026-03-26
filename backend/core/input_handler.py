import os
import yt_dlp
import subprocess
from urllib.parse import urlparse

AUDIO_DIR = "audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

def is_url(input_source:str):
    try:
        result = urlparse(input_source)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_audio_from_url(url: str):
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
        return file_path
    except Exception:
        raise Exception("Unable to download video.Please upload the file manually")
        
            

def convert_video_to_audio(video_path: str):
    audio_path = os.path.splitext(video_path)[0] + ".mp3"

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-ab", "192k",
        "-ar", "44100",
        "-y",
        audio_path
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return audio_path

def handle_input(input_source: str):
    
    if is_url(input_source):
        print("Detected URL input...")
        return download_audio_from_url(input_source)
    
    if input_source.endswith((".mp3", ".wav")):
        print("Detected local audio...")
        return input_source
    
    if input_source.endswith((".mp4", ".mkv",".avi")):
        print("Detected local video..")
        return convert_video_to_audio(input_source)
    
    raise ValueError("Unsupported input format")