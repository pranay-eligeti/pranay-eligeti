"""Qdrant vector store with local in-memory support."""
from __future__ import annotations

from qdrant_client import QdrantClient, models

from .models import DocumentChunk, RetrievalHit


class QdrantVectorStore:
    def __init__(self, dimension: int, collection_name: str = "rag_chunks") -> None:
        self.client = QdrantClient(":memory:")
        self.collection_name = collection_name
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=dimension,
                distance=models.Distance.COSINE,
            ),
        )

    def upsert(self, chunks: list[DocumentChunk], vectors: list[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors must have the same length")
        points = [
            models.PointStruct(
                id=index,
                vector=vector,
                payload={
                    "chunk_id": chunk.chunk_id,
                    "source": chunk.source,
                    "text": chunk.text,
                    "metadata": chunk.metadata,
                },
            )
            for index, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, vector: list[float], limit: int = 5) -> list[RetrievalHit]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=limit,
            with_payload=True,
        ).points
        return [
            RetrievalHit(
                chunk_id=point.payload["chunk_id"],
                source=point.payload["source"],
                text=point.payload["text"],
                score=float(point.score),
                metadata=point.payload.get("metadata", {}),
            )
            for point in results
        ]
