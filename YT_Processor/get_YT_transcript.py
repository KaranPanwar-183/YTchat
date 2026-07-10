import os
import re

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

TRANSCRIPT_DIR = "transcribed_texts"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


def extract_video_id(url: str) -> str:
    """
    Extract the 11-character YouTube video ID from a URL.
    """
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:[&?/]|$)",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract a video ID from URL: {url}")


def get_youtube_transcript(url: str, languages=("en", "hi")) -> str:
    """
    Fetch the transcript/captions for a YouTube video and save it as a
    plain-text file.

    NOTE: youtube-transcript-api v1.x changed to an instance-based API.
    YouTubeTranscriptApi.list_transcripts(...) (classmethod, old API) no
    longer exists. Use YouTubeTranscriptApi().list(...) / .fetch(...) instead.
    """
    video_id = extract_video_id(url)
    ytt_api = YouTubeTranscriptApi()

    try:
        try:
            fetched_transcript = ytt_api.fetch(video_id, languages=list(languages))
        except NoTranscriptFound:
            # None of our preferred languages exist for this video --
            # fall back to whatever caption track IS available.
            transcript_list = ytt_api.list(video_id)
            available_codes = [t.language_code for t in transcript_list]
            fetched_transcript = ytt_api.fetch(video_id, languages=available_codes)
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        raise RuntimeError(
            f"No captions/transcript are available for this video ({video_id}): {e}"
        ) from e

    entries = fetched_transcript.to_raw_data()
    text = " ".join(entry["text"] for entry in entries)

    transcript_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(text)

    return transcript_path


def process_youtube_transcript(url: str) -> str:
    """
    Fetch and save the transcript for a YouTube URL.
    """
    print("Fetching transcript...")
    transcript_path = get_youtube_transcript(url)
    print("Transcript fetched!")
    return transcript_path


if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ")
    path = process_youtube_transcript(youtube_url)
    print("\nSaved transcript:")
    print(path)