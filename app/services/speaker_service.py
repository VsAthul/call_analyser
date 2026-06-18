import json
from app.core.logger import logger
from app.services.groq_service import generate_response



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

    Return ONLY valid JSON.

    Format:

    [
        {{
            "speaker": "Customer",
            "text": "..."
        }}
    ]

    Transcript:

    {transcript_text}
    """
    try:
        logger.info(
    "Starting speaker mapping"
)
        response: str = generate_response(
            prompt=prompt,
            temperature=0
        )
    except Exception as e:
        logger.exception(
        "Speaker mapping LLM call failed"
    )
        raise RuntimeError(
            f"Speaker mapping failed: {e}"
        )

    try:

        mapped_segments: list[dict] = (
            json.loads(response)
        )

        return mapped_segments

    except Exception:
        logger.warning(
    "Invalid JSON from speaker mapping. Using fallback speaker assignment."
)
        fallback_segments: list[dict] = []

        for item in transcript_segments:

            fallback_segments.append(
                {
                    "speaker": "Customer",
                    "text": item["text"]
                }
            )

        return fallback_segments