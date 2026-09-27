"""Simple overlapping text chunker."""
from __future__ import annotations

import hashlib

from .models import DocumentChunk


def chunk_text(text: str, source: str, chunk_size: int = 120, overlap: int = 20) -> list[DocumentChunk]:
    words = text.split()
    if not words:
        return []
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > 0 and 0 <= overlap < chunk_size")

    step = chunk_size - overlap
    chunks: list[DocumentChunk] = []

    for start in range(0, len(words), step):
        body = " ".join(words[start : start + chunk_size]).strip()
        if not body:
            continue
        digest = hashlib.sha1(f"{source}:{start}:{body}".encode("utf-8")).hexdigest()[:12]
        chunks.append(
            DocumentChunk(
                chunk_id=f"{source}:{digest}",
                source=source,
                text=body,
                metadata={"start_word": start, "end_word": min(start + chunk_size, len(words))},
            )
        )
        if start + chunk_size >= len(words):
            break

    return chunks
