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
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": False,
        # Extra safety net: sanitizes any remaining template fields against
        # unsafe characters, in case other templates are added later.
        "restrictfilenames": True,
        # YouTube frequently returns 403 for the "web" client on datacenter/cloud
        # IPs (like Streamlit Cloud). Forcing the android client first bypasses
        # the signature/throttling check that triggers it in most cases, with
        # "web" as a fallback if android fails for a given video.
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"],
            }
        },
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"
            )
        },
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