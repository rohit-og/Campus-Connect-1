from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from config import (
    QDRANT_API_KEY,
    QDRANT_COLLECTION_CANDIDATES,
    QDRANT_COLLECTION_JOBS,
    QDRANT_URL,
)


_qdrant_client: Optional[QdrantClient] = None


def get_qdrant_client() -> QdrantClient:
    """Singleton accessor for Qdrant client."""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY or None,
        )
    return _qdrant_client


def ensure_collections(vector_size: int) -> None:
    """
    Ensure that the standard collections for jobs and candidates exist.

    This is safe to call multiple times; it will only create collections if needed.
    """
    client = get_qdrant_client()

    for name in (QDRANT_COLLECTION_JOBS, QDRANT_COLLECTION_CANDIDATES):
        try:
            client.get_collection(name)
            # Collection exists
            continue
        except Exception:
            # Create collection
            client.recreate_collection(
                collection_name=name,
                vectors_config=qm.VectorParams(
                    size=vector_size,
                    distance=qm.Distance.COSINE,
                ),
            )


def upsert_points(
    collection: str,
    ids: List[str],
    vectors: List[List[float]],
    payloads: List[Dict[str, Any]],
) -> None:
    """Upsert points into a given collection."""
    client = get_qdrant_client()
    if not ids:
        return
    client.upsert(
        collection_name=collection,
        points=[
            qm.PointStruct(id=pid, vector=vec, payload=payload)
            for pid, vec, payload in zip(ids, vectors, payloads)
        ],
    )


def search(
    collection: str,
    query_vector: List[float],
    top_k: int = 10,
    filter_: Optional[qm.Filter] = None,
) -> List[qm.ScoredPoint]:
    """Search a collection by vector similarity."""
    client = get_qdrant_client()
    return client.search(
        collection_name=collection,
        query_vector=query_vector,
        limit=top_k,
        query_filter=filter_,
    )

