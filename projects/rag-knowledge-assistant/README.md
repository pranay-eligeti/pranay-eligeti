# RAG Knowledge Assistant

> A testable Retrieval-Augmented Generation pipeline with chunking, embeddings, Qdrant vector search, citation-aware retrieval, and an optional Claude answer layer.

## What this demonstrates

This portfolio project focuses on the engineering around RAG rather than only the final model call:

- text chunking with overlap
- pluggable embedding providers
- Qdrant vector storage and similarity search
- metadata carried with retrieved chunks
- citation-aware context assembly
- deterministic extractive mode for CI
- optional Claude generation for grounded answers
- a local architecture that can later move to managed infrastructure

Qdrant currently documents an in-memory client for local experimentation and the query_points API for similarity search.

## Architecture

```text
Documents
   |
   v
Chunking + metadata
   |
   v
Embedding provider
   |
   v
Qdrant vector store
   |
   v
Query embedding
   |
   v
Top-k retrieval
   |
   +--> citations + source metadata
   |
   v
Grounded context
   |
   +--> extractive answer
   |
   +--> optional Claude answer
```

## Project structure

```text
rag-knowledge-assistant/
├── .github/workflows/rag-ci.yml
├── sample_data/handbook.md
├── src/
│   ├── __init__.py
│   ├── chunker.py
│   ├── demo.py
│   ├── embeddings.py
│   ├── models.py
│   ├── rag.py
│   └── vector_store.py
├── tests/test_rag.py
├── .env.example
├── pyproject.toml
└── README.md
```

## Quick start

```bash
cd projects/rag-knowledge-assistant
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev]"
pytest -q
```

Run the deterministic demo:

```bash
python -m src.demo
```

The default demo uses a deterministic hash-based embedding provider, so it runs without API credentials.

Qdrant supports local in-memory mode, so the demo does not require a separate Qdrant server.

## Embedding providers

### Deterministic CI provider

HashEmbeddingProvider produces fixed-size normalized vectors without downloading a model or calling an external API. This keeps tests fast and reproducible.

### FastEmbed provider

FastEmbedProvider uses the Qdrant-compatible FastEmbed integration for local semantic embeddings.

## Optional Claude generation

Set:

```env
ANTHROPIC_API_KEY=...
RAG_MODEL=...
```

Then use ClaudeAnswerer with the retrieved hits. Its prompt requires answers to stay within supplied sources and cite claims using [S#].

The public tests never call the external model.

## Retrieval and citations

Each retrieval hit retains:

- chunk ID
- source
- chunk text
- similarity score
- metadata

The answer layer converts hits into source-labelled context such as [S1] and [S2], making generated answers traceable to retrieved material.

## Design principles

**Retrieval before generation**  
The LLM is downstream of retrieval instead of being treated as the knowledge source.

**Explicit interfaces**  
Embedding and storage layers are separated so deterministic testing can later be replaced by real embedding services without rewriting the RAG orchestration.

**Grounded failure mode**  
The extractive path can return retrieved evidence directly rather than inventing an answer when generation is unavailable.

**Production path**  
The next engineering layer is evaluation: retrieval quality, citation correctness, groundedness, regression cases, latency, and token/cost measurement.

## Portfolio note

This repository is the foundation for the next AI engineering stages: evaluation, observability, production API design, Docker/CI, and cloud deployment.

## Author

**Pranay Eligeti**

[LinkedIn](https://www.linkedin.com/in/pranay-eligeti) · [GitHub](https://github.com/pranay-eligeti)
