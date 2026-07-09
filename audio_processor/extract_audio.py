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

    # Path to a Netscape-format cookies file exported from a logged-in YouTube
    # session (see: "Get cookies.txt LOCALLY" browser extension). Required
    # because YouTube now requires a PO Token / authenticated session for most
    # clients' media-stream requests; without it, extract_info succeeds but
    # the actual download step returns HTTP 403.
    COOKIES_PATH = os.path.join(os.path.dirname(__file__), "..", "cookies.txt")

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