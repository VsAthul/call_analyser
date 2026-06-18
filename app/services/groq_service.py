from groq import Groq
from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY


MODEL_NAME: str = "llama-3.1-8b-instant"


client: Groq = Groq(
    api_key=GROQ_API_KEY
)


def generate_response(prompt: str,temperature: float = 0.0) -> str:
    """
    Generate response from Groq.
    Args:
        prompt (str): Prompt text.
        temperature (float): Sampling temperature.

    Returns:
        str: LLM response.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature
    )

    return (
        response
        .choices[0]
        .message.content
    )

def get_llm(temperature: float = 0.0) -> ChatGroq:

    return ChatGroq(
        model=MODEL_NAME,
        api_key=GROQ_API_KEY,
        temperature=temperature
    )