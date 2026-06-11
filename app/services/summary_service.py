from app.services.groq_service import generate_response
from app.core.logger import logger

def generate_summary(transcript_text: str) -> str:
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
    try:
        logger.info(
        "Starting summary generation"
    )
        summary: str = generate_response(
            prompt=prompt,
            temperature=0.2
        )
        return summary
    except Exception:
        logger.exception(
        "Summary generation failed"
    )

    raise

def detect_call_type(transcript_text: str) -> str:
    """
    Detect call type from transcript using LLM.

    Args:
        transcript_text (str)

    Returns:
        str
    """

    prompt: str = f"""
You are a banking call analyst.

Analyze the following call transcript carefully and classify it into 
one of these types:

- Loan Inquiry        (customer asking about loans, EMI, interest rates)
- Account Opening     (customer wants to open a new bank account)
- Account Issue       (problems with existing account, balance, statements)
- Card Services       (credit/debit card related queries or issues)
- Fraud Report        (reporting unauthorized transactions or suspicious activity)
- Fund Transfer       (transferring money, NEFT, RTGS, UPI issues)
- General Inquiry     (general banking questions not fitting other categories)
- Complaint           (customer complaints about service or staff)
- Technical Support   (internet banking, mobile app, OTP issues)

Instructions:
- Read the full transcript carefully before deciding
- Choose the type that best matches the PRIMARY topic of the call
- If the transcript is in Malayalam or any regional language, still classify correctly
- Reply with ONLY the call type name, no explanation, no punctuation

Transcript:
{transcript_text}
"""
    try:
        logger.info(
            "Starting call type detection"
        )
        result = generate_response(
            prompt=prompt,
            temperature=0
        ).strip()
        logger.info(
            f"Call type detected: {result}"
        )

        return result

    except Exception:
        logger.exception(
            "Call type detection failed"
        )
        raise