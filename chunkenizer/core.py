"""
AI RAG Chunkenizer - Core Chunking Engine
Token-aware text splitting for optimal RAG performance.
A product of EPH4™ by VIEWVALUE LLC.

Copyright (c) 2025 VIEWVALUE LLC. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.

NOTICE:
    - EPH4™ is a trademark of VIEWVALUE LLC
    - This software runs entirely locally - no data is transmitted externally
    - No telemetry, analytics, or tracking is performed
    - Token counts are estimates (~4 chars per token) and may vary from actual LLM tokenization
    - Users are responsible for verifying output accuracy for their use case
"""

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
import tiktoken

from .extractors import extract_text, get_supported_extensions


@dataclass
class Chunk:
    """A single chunk of text with metadata."""
    index: int
    text: str
    token_count: int
    char_count: int

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "text": self.text,
            "token_count": self.token_count,
            "char_count": self.char_count
        }


@dataclass
class ChunkResult:
    """Result of chunking a document."""
    source: str
    total_chunks: int
    total_tokens: int
    total_chars: int
    chunks: List[Chunk]
    config: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "total_chunks": self.total_chunks,
            "total_tokens": self.total_tokens,
            "total_chars": self.total_chars,
            "config": self.config,
            "chunks": [c.to_dict() for c in self.chunks]
        }

    def to_texts(self) -> List[str]:
        """Return just the text content of each chunk."""
        return [c.text for c in self.chunks]


class Chunkenizer:
    """
    Token-aware document chunker optimized for RAG pipelines.

    Uses tiktoken for accurate token counting and splits on word
    boundaries to preserve semantic meaning.

    Args:
        max_tokens: Maximum tokens per chunk (default: 1000)
        overlap_tokens: Number of tokens to overlap between chunks (default: 100)
        model: Tiktoken model for tokenization (default: "gpt-4")

    Example:
        >>> chunker = Chunkenizer(max_tokens=500, overlap_tokens=50)
        >>> result = chunker.process("report.pdf")
        >>> print(f"Created {result.total_chunks} chunks")
    """

    SUPPORTED_EXTENSIONS = get_supported_extensions()

    def __init__(
        self,
        max_tokens: int = 1000,
        overlap_tokens: int = 100,
        model: str = "gpt-4"
    ):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.model = model
        self._encoding = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        return len(self._encoding.encode(text))

    def chunk_text(self, text: str) -> List[Chunk]:
        """
        Split text into token-aware chunks with overlap.

        The algorithm:
        1. Split text into words
        2. Accumulate words until max_tokens is reached
        3. Save chunk and start new one with overlap
        4. Repeat until all text is processed

        Args:
            text: Raw text to chunk

        Returns:
            List of Chunk objects
        """
        if not text or not text.strip():
            return []

        words = text.split()
        chunks = []
        current_words = []
        current_tokens = 0

        for word in words:
            word_tokens = len(self._encoding.encode(word + " "))

            # Check if adding this word exceeds limit
            if current_tokens + word_tokens > self.max_tokens and current_words:
                # Save current chunk
                chunk_text = " ".join(current_words)
                chunks.append(Chunk(
                    index=len(chunks),
                    text=chunk_text,
                    token_count=self.count_tokens(chunk_text),
                    char_count=len(chunk_text)
                ))

                # Calculate overlap in words (approximate)
                overlap_word_count = max(1, self.overlap_tokens // 4)  # ~4 chars per token avg
                current_words = current_words[-overlap_word_count:]
                current_tokens = sum(
                    len(self._encoding.encode(w + " "))
                    for w in current_words
                )

            current_words.append(word)
            current_tokens += word_tokens

        # Don't forget the last chunk
        if current_words:
            chunk_text = " ".join(current_words)
            chunks.append(Chunk(
                index=len(chunks),
                text=chunk_text,
                token_count=self.count_tokens(chunk_text),
                char_count=len(chunk_text)
            ))

        return chunks

    def process(self, file_path: str) -> ChunkResult:
        """
        Process a document file and return chunks.

        Supports: PDF, DOCX, XLSX, CSV, PPTX

        Args:
            file_path: Path to the document file

        Returns:
            ChunkResult with all chunks and metadata
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported format: {ext}. "
                f"Supported: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        # Extract text from document
        text = extract_text(file_path)

        # Chunk the text
        chunks = self.chunk_text(text)

        return ChunkResult(
            source=path.name,
            total_chunks=len(chunks),
            total_tokens=sum(c.token_count for c in chunks),
            total_chars=sum(c.char_count for c in chunks),
            chunks=chunks,
            config={
                "max_tokens": self.max_tokens,
                "overlap_tokens": self.overlap_tokens,
                "model": self.model
            }
        )

    def process_text(self, text: str, source_name: str = "text") -> ChunkResult:
        """
        Process raw text directly (no file).

        Args:
            text: Raw text to chunk
            source_name: Name to identify the source

        Returns:
            ChunkResult with all chunks and metadata
        """
        chunks = self.chunk_text(text)

        return ChunkResult(
            source=source_name,
            total_chunks=len(chunks),
            total_tokens=sum(c.token_count for c in chunks),
            total_chars=sum(c.char_count for c in chunks),
            chunks=chunks,
            config={
                "max_tokens": self.max_tokens,
                "overlap_tokens": self.overlap_tokens,
                "model": self.model
            }
        )
