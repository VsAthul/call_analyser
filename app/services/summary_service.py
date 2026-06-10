from app.services.groq_service import generate_response


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

    return generate_response(prompt=prompt, temperature=0).strip()