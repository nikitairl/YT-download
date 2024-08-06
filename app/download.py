import shutil
import logging

from fastapi import HTTPException
from pytubefix import YouTube
from pytubefix.cli import on_progress

from utils import merge_audio_video


class Downloader:
    DOWNLOAD_TMP_DIR = "./downloads/tmp/"
    AUDIO_DIR = "./downloads/audio/"
    VIDEO_DIR = "./downloads/video (no sound)/"

    def __init__(
        self, url: str, resolution: str = "1080"
    ):
        self.url = url
        try:
            self.yt = YouTube(self.url, on_progress_callback=on_progress)
        except Exception as e:
            logging.error(f"Failed to initialize Youtube object: {e}")
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        self.resolution = resolution + "p"

    def audio_download(self, path: str = AUDIO_DIR):
        try:
            audio_stream = self.yt.streams.get_audio_only()
            if audio_stream:
                audio_stream.download(
                    path, skip_existing=True, filename=self.yt.title + ".mp3"
                )
            else:
                logging.warning("No audio stream found")
        except Exception as e:
            logging.error(f"Audio download failed: {e}")
            raise HTTPException(
                status_code=500,
                detail="Audio download failed, make sure the URL is valid",
            )

    def video_download(self, path: str = VIDEO_DIR):
        try:
            video_stream = self.yt.streams.filter(
                res=self.resolution, is_dash=True
            ).first()
            if video_stream:
                video_stream.download(
                    path, skip_existing=True, filename=self.yt.title + ".mp4"
                )
            else:
                logging.warning(
                    "No video stream found for the specified resolution"
                )
        except Exception as e:
            logging.error(f"Video download failed: {e}")
            raise HTTPException(
                status_code=500, detail="Video download failed"
            )

    def full_download(self):
        try:
            self.audio_download(path=self.DOWNLOAD_TMP_DIR)
            self.video_download(path=self.DOWNLOAD_TMP_DIR)
            merge_audio_video(self.yt.title + ".mp3", self.yt.title + ".mp4")
            shutil.rmtree(self.DOWNLOAD_TMP_DIR)
        except Exception as e:
            logging.error(f"Full download failed: {e}")
            raise HTTPException(status_code=500, detail="Full download failed")
