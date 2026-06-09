from app.services.groq_service import generate_response
from app.services.chroma_service import retrieve_chunks


from app.services.groq_service import generate_response



def answer_question(
    call_id: int,
    question: str
) -> str:
    """
    RAG Question Answering.

    Args:
        call_id (int)
        question (str)

    Returns:
        str
    """

    chunks: list[str] = retrieve_chunks(
        call_id=call_id,
        query=question
    )

    context: str = "\n\n".join(
        chunks
    )

    prompt: str = f"""
You are a banking call analyst.

Answer ONLY using the context.

Context:
{context}

Question:
{question}
"""

    answer: str = generate_response(
        prompt=prompt,
        temperature=0
    )

    return answer