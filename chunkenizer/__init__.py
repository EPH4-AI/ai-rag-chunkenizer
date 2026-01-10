"""
AI Chunkenizer - Fast, token-aware document chunking for RAG pipelines.
A product of EPH4™ by VIEWVALUE LLC.

Copyright (c) 2025 VIEWVALUE LLC. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.

EPH4™ is a trademark of VIEWVALUE LLC.

DISCLAIMER:
    This software is provided "as is" without warranty of any kind.
    VIEWVALUE LLC is not responsible for any damages arising from use of this software.
    Users are solely responsible for compliance with applicable laws and regulations.
    This software does not collect, transmit, or store any user data.
    All processing occurs locally on the user's machine.

Usage:
    from chunkenizer import Chunkenizer

    chunker = Chunkenizer(max_tokens=1000, overlap_tokens=100)
    result = chunker.process("document.pdf")

    for chunk in result.chunks:
        print(chunk.text)

For more information: https://github.com/EPH4-AI/ai-chunkenizer
"""

from .core import Chunkenizer, ChunkResult, Chunk
from .extractors import extract_text

__version__ = "1.0.0"
__all__ = ["Chunkenizer", "ChunkResult", "Chunk", "extract_text"]
