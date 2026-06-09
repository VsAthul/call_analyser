from app.services.groq_service import (
    generate_response
)


def generate_summary(
    transcript_text: str
) -> str:
    """
    Generate call summary.

    Args:
        transcript_text (str)

    Returns:
        str
    """

    prompt: str = f"""
You are a banking call summarizer.

Create a concise summary.

Transcript:

{transcript_text}
"""

    summary: str = generate_response(
        prompt=prompt,
        temperature=0.2
    )

    return summary