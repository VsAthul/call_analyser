from faster_whisper import WhisperModel

from app.core.config import WHISPER_MODEL


model: WhisperModel = WhisperModel(
    WHISPER_MODEL,
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(
    audio_path: str
) -> list[dict]:
    """
    Transcribe audio file.

    Args:
        audio_path (str)

    Returns:
        list[dict]
    """

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