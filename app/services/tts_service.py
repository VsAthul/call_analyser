from pathlib import Path

from gtts import gTTS


def generate_audio_summary(
    summary: str,
    output_path: str,
    language: str = "en"
) -> str:
    """
    Convert summary to speech.

    Args:
        summary (str)
        output_path (str)
        language (str)

    Returns:
        str
    """

    tts = gTTS(
        text=summary,
        lang=language
    )

    tts.save(output_path)

    return output_path