def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list[str]:
    """
    Split transcript into chunks.

    Args:
        text (str)
        chunk_size (int)
        chunk_overlap (int)

    Returns:
        list[str]
    """

    chunks: list[str] = []

    start: int = 0

    while start < len(text):

        end: int = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += (
            chunk_size - chunk_overlap
        )

    return chunks