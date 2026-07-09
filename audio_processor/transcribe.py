import whisper
import os


TRANSCRIPT_DIR = "transcribed_texts"

model = whisper.load_model("tiny")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

def transcribe_audio(audio_path: str) -> str:
  file_name = os.path.splitext(os.path.basename(audio_path))[0]
  result = model.transcribe(audio_path, language="en")
  transcript_path = os.path.join(TRANSCRIPT_DIR, f"{file_name}.txt")
  with open(transcript_path, "w", encoding="utf-8") as f:
    f.write(result["text"])
  print(f"Transcription completed! Transcript saved to: {transcript_path}") 
  return transcript_path