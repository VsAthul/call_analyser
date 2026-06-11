import chromadb
from app.core.logger import logger
from app.core.config import CHROMA_DB_PATH

try:
    client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH
    )

    collection = client.get_or_create_collection(
        name="transcript_embeddings"
    )
    logger.info(
    f"ChromaDB initialized. path={CHROMA_DB_PATH}"
)
except Exception as e:
    logger.exception(
        "Failed to initialize ChromaDB"
    )
    raise RuntimeError(
        f"Failed to initialize ChromaDB: {e}"
    )

def store_chunks(call_id: int,chunks: list[str]) -> None:
    """
    Store chunks in ChromaDB.

    Args:
        call_id (int)
        chunks (list[str])

    Returns:
        None
    """
    if not chunks:
        raise ValueError(
            "No chunks provided for storage"
        )

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
    try:
        collection.add(
                ids=ids,
                documents=chunks,
                metadatas=metadatas
            )
        logger.info(
            f"Stored {len(chunks)} chunks for call_id={call_id}"
        )
    except Exception:
        logger.exception(
        f"Failed to store chunks for call_id={call_id}"
    )
        raise

def retrieve_chunks(call_id: int,query: str,top_k: int = 5) -> list[str]:
    """
    Retrieve relevant chunks.

    Args:
        call_id (int)
        query (str)
        top_k (int)

    Returns:
        list[str]
    """
    try:
        result = collection.query(
            query_texts=[query],
            n_results=top_k,
            where={
                "call_id": call_id
            }
        )
    except Exception:
        logger.exception(
        f"Failed to retrieve chunks for call_id={call_id}"
    )
        raise


    documents: list[str] = (
        result["documents"][0]
    )

    return documents