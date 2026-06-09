import chromadb

from app.core.config import (
    CHROMA_DB_PATH
)

client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name="transcript_embeddings"
)


def store_chunks(
    call_id: int,
    chunks: list[str]
) -> None:
    """
    Store chunks in ChromaDB.

    Args:
        call_id (int)
        chunks (list[str])

    Returns:
        None
    """

    ids: list[str] = []
    metadatas: list[dict] = []

    for index, _ in enumerate(chunks):

        ids.append(
            f"{call_id}_{index}"
        )

        metadatas.append(
            {
                "call_id": call_id,
                "chunk_index": index
            }
        )

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )
def retrieve_chunks(
    call_id: int,
    query: str,
    top_k: int = 5
) -> list[str]:
    """
    Retrieve relevant chunks.

    Args:
        call_id (int)
        query (str)
        top_k (int)

    Returns:
        list[str]
    """

    result = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={
            "call_id": call_id
        }
    )

    documents: list[str] = (
        result["documents"][0]
    )

    return documents