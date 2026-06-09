from sentence_transformers import (
    SentenceTransformer
)

embedding_model: SentenceTransformer = (
    SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )
)


def generate_embedding(
    text: str
) -> list[float]:
    """
    Generate embedding vector.

    Args:
        text (str)

    Returns:
        list[float]
    """

    vector: list[float] = (
        embedding_model.encode(text)
        .tolist()
    )

    return vector