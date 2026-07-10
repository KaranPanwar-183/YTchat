import os
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = "downloads"
COOKIES_PATH = os.path.join(os.path.dirname(__file__), "..", "cookies.txt")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def _ensure_cookies_file():
    """
    Ensure cookies.txt exists on disk before yt-dlp needs it.

    Locally: if you already have a cookies.txt at the repo root, this does
    nothing and it's used as-is.

    On Streamlit Cloud: cookies.txt is gitignored (never committed), so this
    writes it out at runtime from Streamlit Secrets (st.secrets["YOUTUBE_COOKIES"]),
    which you set in the app's Settings -> Secrets panel.
    """
    if os.path.exists(COOKIES_PATH):
        return

    try:
        import streamlit as st
        cookies_content = st.secrets.get("YOUTUBE_COOKIES")
    except Exception:
        cookies_content = None

    if cookies_content:
        with open(COOKIES_PATH, "w", encoding="utf-8") as f:
            f.write(cookies_content)


def download_audio(url: str) -> str:
    """
    Download the best available audio from a YouTube video.

    Args:
        url: YouTube video URL

    Returns:
        Path to the downloaded audio file.
    """

    _ensure_cookies_file()

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": False,
        # Extra safety net: sanitizes any remaining template fields against
        # unsafe characters, in case other templates are added later.
        "restrictfilenames": True,
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

    if os.path.exists(COOKIES_PATH):
        ydl_opts["cookiefile"] = COOKIES_PATH
    else:
        print(
            f"WARNING: cookies file not found at {COOKIES_PATH}. "
            "YouTube downloads may fail with HTTP 403 without it."
        )

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