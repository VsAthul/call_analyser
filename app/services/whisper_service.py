from faster_whisper import WhisperModel
from app.core.config import WHISPER_MODEL
import os

try:
    model = WhisperModel(
        WHISPER_MODEL,
        device="cpu",
        compute_type="int8"
    )
except Exception as e:
    raise RuntimeError(
        f"Failed to initialize Whisper model: {e}"
    )


def transcribe_audio(audio_path: str) -> list[dict]:
    """
    Transcribe audio file.

    Args:
        audio_path (str)

    Returns:
        list[dict]
    """
    if not isinstance(audio_path, str):
        raise TypeError(
            "audio_path must be a string"
        )
    if not os.path.exists(audio_path):
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )
    try:
        segments, _ = model.transcribe(
            audio_path
        )

        transcript_segments: list[dict] = []

        for segment in segments:

            transcript_segments.append(
                {
                    "start": float(segment.start),
                    "end": float(segment.end),
                    "text": segment.text.strip()
                }
            )

        return transcript_segments
    except Exception as e:
        raise RuntimeError(
            f"Audio transcription failed: {str(e)}"
        )