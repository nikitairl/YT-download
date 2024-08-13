import logging
import os
import shutil

import ffmpeg
from fastapi import HTTPException
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.innertube import _default_clients

from constants import DOWNLOAD_TMP_DIR, AUDIO_DIR, VIDEO_DIR

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


class Downloader:
    DOWNLOAD_TMP_DIR = DOWNLOAD_TMP_DIR
    AUDIO_DIR = AUDIO_DIR
    VIDEO_DIR = VIDEO_DIR

    def __init__(self, url: str, resolution: str = "720"):
        self.url = url
        self.audio = None
        self.video = None
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
            self.merge_audio_video(
                self.yt.title + ".mp3", self.yt.title + ".mp4"
            )
            self.cleanup()
        except Exception as e:
            logging.error(f"Full download failed: {e}")
            raise HTTPException(status_code=500, detail="Full download failed")

    def merge_audio_video(self, audio_title, video_title):
        try:
            input_video = ffmpeg.input(self.DOWNLOAD_TMP_DIR + video_title)
            input_audio = ffmpeg.input(self.DOWNLOAD_TMP_DIR + audio_title)
            ffmpeg.concat(input_video, input_audio, v=1, a=1).output(
                "./downloads/" + video_title
            ).run()
        except Exception as e:
            logging.error(f"Audio and video merge failed: {e}")
            raise HTTPException(
                status_code=500, detail="Audio and video merge failed"
            )

    @staticmethod
    def cleanup():
        if os.path.exists(DOWNLOAD_TMP_DIR):
            shutil.rmtree(DOWNLOAD_TMP_DIR)
