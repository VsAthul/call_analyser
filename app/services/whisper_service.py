from faster_whisper import WhisperModel
from app.core.config import WHISPER_MODEL
import os
from app.core.logger import logger

try:
    model = WhisperModel(
        WHISPER_MODEL,
        device="cpu",
        compute_type="int8"
    )
    logger.info(
        f"Whisper model loaded: {WHISPER_MODEL}"
    )
except Exception as e:
    logger.exception(
        "Failed to initialize Whisper model"
    )
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
    logger.info(
        f"Starting transcription: {audio_path}"
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
        if not transcript_segments:
            raise ValueError(
                "Audio contains no detectable speech"
            )
        logger.info(
            f"Transcription completed. Segments={len(transcript_segments)}"
        )

        return transcript_segments
    except Exception as e:
        logger.exception(
            f"Transcription failed: {audio_path}"
        )
        raise RuntimeError(
            f"Audio transcription failed: {str(e)}"
        )