def transcript_to_text(
    transcript: list[dict]
) -> str:
    """
    Convert transcript segments
    into single string.

    Args:
        transcript (list[dict])

    Returns:
        str
    """

    return "\n".join(
        [
            f"{item['speaker']}: {item['text']}"
            for item in transcript
        ]
    )