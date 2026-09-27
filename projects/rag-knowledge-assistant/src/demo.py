"""Run the deterministic local RAG demonstration."""
from __future__ import annotations
from pathlib import Path
from .embeddings import HashEmbeddingProvider
from .rag import RagEngine
from .vector_store import QdrantVectorStore

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = ROOT / "sample_data" / "handbook.md"
    text = source.read_text(encoding="utf-8")
    embedder = HashEmbeddingProvider()
    engine = RagEngine(embedder, QdrantVectorStore(embedder.dimension))
    engine.ingest([("handbook.md", text)])
    answer = engine.extractive_answer("How should provider data be prepared before deduplication?", top_k=3)
    print("Answer:")
    print(answer.answer)
    print("\nCitations:")
    print(", ".join(answer.citations))


if __name__ == "__main__":
    main()
