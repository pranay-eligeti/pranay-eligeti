from src.chunker import chunk_text
from src.embeddings import HashEmbeddingProvider
from src.models import GroundedAnswer
from src.rag import RagEngine
from src.vector_store import QdrantVectorStore


def make_engine():
    embedder = HashEmbeddingProvider(dimension=256)
    store = QdrantVectorStore(dimension=embedder.dimension)
    return RagEngine(embedder, store)


def test_chunker_preserves_source_and_creates_chunks():
    chunks = chunk_text("one two three four five six seven eight nine ten", "handbook.md", chunk_size=5, overlap=1)
    assert len(chunks) == 3
    assert all(chunk.source == "handbook.md" for chunk in chunks)


def test_rag_returns_citations_and_hits():
    engine = make_engine()
    engine.ingest([
        ("approvals.md", "Production workflow actions require explicit approval before dispatch."),
        ("data.md", "Provider data should be normalized before deduplication."),
    ])
    answer = engine.extractive_answer("What is required before workflow dispatch?", top_k=2)
    assert isinstance(answer, GroundedAnswer)
    assert answer.hits
    assert answer.citations
    assert answer.citations[0] == "[S1]"
    assert "approval" in answer.answer.lower()


def test_empty_retrieval_is_grounded():
    engine = make_engine()
    engine.ingest([("a.md", "Python testing improves reliability.")])
    answer = engine.extractive_answer("quantum gardening", top_k=1)
    assert answer.query == "quantum gardening"
    assert answer.answer
