"""RAG orchestration and citation-aware answer generation."""
from __future__ import annotations

import os
from typing import Iterable

from anthropic import Anthropic

from .chunker import chunk_text
from .embeddings import EmbeddingProvider
from .models import DocumentChunk, GroundedAnswer, RetrievalHit
from .vector_store import QdrantVectorStore


class RagEngine:
    def __init__(self, embedder: EmbeddingProvider, store: QdrantVectorStore) -> None:
        self.embedder = embedder
        self.store = store

    def ingest(self, documents: Iterable[tuple[str, str]]) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []
        for source, text in documents:
            chunks.extend(chunk_text(text, source))
        vectors = self.embedder.embed([chunk.text for chunk in chunks])
        self.store.upsert(chunks, vectors)
        return chunks

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalHit]:
        vector = self.embedder.embed([query])[0]
        return self.store.search(vector, limit=top_k)

    def build_context(self, hits: list[RetrievalHit]) -> tuple[str, list[str]]:
        parts: list[str] = []
        citations: list[str] = []
        for index, hit in enumerate(hits, start=1):
            citation = f"[S{index}]"
            citations.append(citation)
            parts.append(f"{citation} {hit.source}\n{hit.text}")
        return "\n\n".join(parts), citations

    def extractive_answer(self, query: str, top_k: int = 3) -> GroundedAnswer:
        hits = self.retrieve(query, top_k=top_k)
        context, citations = self.build_context(hits)
        answer = context or "No relevant source material was retrieved."
        return GroundedAnswer(query=query, answer=answer, citations=citations, hits=hits)


class ClaudeAnswerer:
    def __init__(self, model: str | None = None) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not configured")
        self.client = Anthropic(api_key=api_key)
        self.model = model or os.environ.get("RAG_MODEL")
        if not self.model:
            raise RuntimeError("RAG_MODEL is not configured")

    def answer(self, query: str, hits: list[RetrievalHit]) -> str:
        context = "\n\n".join(
            f"[S{i}] {hit.source}\n{hit.text}"
            for i, hit in enumerate(hits, start=1)
        )
        prompt = (
            "Answer the question using only the supplied sources. "
            "Cite claims with [S#]. If the sources do not contain the answer, say so. "
            "Do not invent facts.\n\n"
            f"Question: {query}\n\nSources:\n{context}"
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        return getattr(response.content[0], "text", str(response.content[0])).strip()
