
import os
import yt_dlp
from src.utils.config_loader import load_config

class AudioDownloader:
    def __init__(self, output_dir="data/raw"):
        self.output_dir = output_dir
        self.config = load_config()
        os.makedirs(self.output_dir, exist_ok=True)

    def download_track(self, video_url, track_id):
        output_template = os.path.join(self.output_dir, f"{track_id}.%(ext)s")
        expected_file = os.path.join(self.output_dir, f"{track_id}.wav")
        if os.path.exists(expected_file):
            print(f" File already exists: {track_id}")
            return expected_file

        print(f" Downloading: {track_id}...")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            print(f" Download complete: {track_id}")
            return expected_file
        except Exception as e:
            print(f" Error downloading {track_id}: {str(e)}")
            return None
