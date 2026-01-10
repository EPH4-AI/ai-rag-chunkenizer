"""
AI RAG Chunkenizer - Basic Usage Example

Copyright (c) 2025 VIEWVALUE LLC. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.

This example demonstrates basic usage of the AI RAG Chunkenizer library.
All processing happens locally on your machine.
"""

from chunkenizer import Chunkenizer


def main():
    # Initialize chunker with default settings
    chunker = Chunkenizer(
        max_tokens=1000,      # Max tokens per chunk
        overlap_tokens=100    # Overlap for context continuity
    )

    # Process a document
    # Uncomment and replace with your file path:
    # result = chunker.process("path/to/your/document.pdf")

    # Or process raw text directly
    sample_text = """
    This is a sample document that demonstrates how the AI RAG Chunkenizer
    works. It will split this text into smaller chunks that are suitable
    for embedding models and RAG pipelines.

    The chunker respects word boundaries, so you won't see words split
    in the middle. It also maintains overlap between chunks to preserve
    context across boundaries.

    This is particularly useful when processing large documents for
    question-answering systems, semantic search, or any application
    that requires splitting text into manageable pieces.
    """

    result = chunker.process_text(sample_text, source_name="sample.txt")

    # Display results
    print(f"Source: {result.source}")
    print(f"Total chunks: {result.total_chunks}")
    print(f"Total tokens: {result.total_tokens}")
    print(f"Total characters: {result.total_chars}")
    print()

    # Show each chunk
    for chunk in result.chunks:
        print(f"--- Chunk {chunk.index + 1} ({chunk.token_count} tokens) ---")
        print(chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text)
        print()

    # Export to dict (for JSON serialization)
    data = result.to_dict()
    print(f"Exportable keys: {list(data.keys())}")

    # Get just the text content
    texts = result.to_texts()
    print(f"Got {len(texts)} text strings for embedding")


if __name__ == "__main__":
    main()
