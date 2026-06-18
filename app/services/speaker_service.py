import json
from app.core.logger import logger
# from app.services.groq_service import generate_response
from app.schemas.upload_schema import SpeakerMapping, SpeakerSegment
from app.services.groq_service import get_llm



def map_speakers(transcript_segments: list[dict]) -> list[dict]:
    """
    Map transcript segments to Customer/Banker.
    Args:
        transcript_segments (list[dict])
    Returns:
        list[dict]
    """
    if not transcript_segments:
        raise ValueError(
            "No transcript segments provided"
        )
    transcript_text: str = "\n".join(
        [
            item["text"]
            for item in transcript_segments
        ]
    )

    prompt: str = f"""
    You are a banking call analyst.

    Identify whether each sentence
    belongs to:

    1. Customer
    2. Banker

    For every sentence, identify whether the speaker is:

1. Customer
2. Banker

Preserve the original text.
Return all transcript segments.

    Transcript:

    {transcript_text}
    """
    try:

        logger.info(
            "Starting speaker mapping"
        )

        llm = get_llm(
            temperature=0
        )

        structured_llm = (
            llm.with_structured_output(
                SpeakerMapping
            )
        )

        result: SpeakerMapping = (
            structured_llm.invoke(
                prompt
            )
        )

    except Exception as e:

        logger.exception(
            "Speaker mapping LLM call failed"
        )

        raise RuntimeError(
            f"Speaker mapping failed: {e}"
        )

    try:

        mapped_segments = [
            {
                "speaker": segment.speaker,
                "text": segment.text
            }

            for segment in result.segments
        ]

        return mapped_segments

    except Exception as e:

        logger.exception(
            "Failed to process structured speaker mapping"
        )

        raise RuntimeError(
            f"Speaker mapping processing failed: {e}"
    )