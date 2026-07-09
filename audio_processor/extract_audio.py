import os
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_audio(url: str) -> str:
    """
    Download the best available audio from a YouTube video.

    Args:
        url: YouTube video URL

    Returns:
        Path to the downloaded audio file.
    """

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return file_path


def process_youtube_audio(url: str) -> str:
    """
    Download audio from a YouTube URL.

    Args:
        url: YouTube video URL

    Returns:
        Path to the downloaded audio file.
    """

    print("Downloading audio...")

    audio_path = download_audio(url)

    print("Download completed!")

    return audio_path


if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ")

    audio_path = process_youtube_audio(youtube_url)

    print("\nDownloaded audio:")
    print(audio_path)