import os
import yt_dlp
import subprocess
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

TEMP_AUDIO = "temp_audio.mp3"


def is_url(input_source: str):
    try:
        result = urlparse(input_source)
        return result.scheme in ["http", "https"] and result.netloc != ""
    except:
        return False


def download_audio_from_url(url: str):
    logging.info("Downloading from URL...")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "temp_video.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        audio_path = convert_video_to_audio(video_path)

        if os.path.exists(video_path):
            os.remove(video_path)

        return audio_path

    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")


def convert_video_to_audio(video_path: str):
    logging.info("Converting video to audio...")

    audio_path = TEMP_AUDIO

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


def handle_input(input_source: str):

    input_lower = input_source.lower()


    if is_url(input_source):
        return download_audio_from_url(input_source)


    if input_lower.endswith((".mp3", ".wav")):
        return input_source

    if input_lower.endswith((".mp4", ".mkv", ".avi", ".mov", ".webm")):
        return convert_video_to_audio(input_source)

    raise ValueError("Unsupported input format")