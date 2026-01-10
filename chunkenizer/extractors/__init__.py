"""
AI Chunkenizer - Document Extractors
Text extraction for PDF, Word, Excel, CSV, and PowerPoint files.
A product of EPH4™ by VIEWVALUE LLC.

Copyright (c) 2025 VIEWVALUE LLC. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.

EPH4™ is a trademark of VIEWVALUE LLC.

NOTICE:
    All extraction happens locally using open-source libraries.
    No files are uploaded or transmitted to external services.
"""

from pathlib import Path
from typing import Set

from .pdf import extract_pdf
from .docx import extract_docx
from .xlsx import extract_xlsx
from .csv_extractor import extract_csv
from .pptx import extract_pptx


EXTRACTORS = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".xlsx": extract_xlsx,
    ".xls": extract_xlsx,
    ".csv": extract_csv,
    ".pptx": extract_pptx,
}


def get_supported_extensions() -> Set[str]:
    """Return set of supported file extensions."""
    return set(EXTRACTORS.keys())


def extract_text(file_path: str) -> str:
    """
    Extract text from a document file.

    Args:
        file_path: Path to the document

    Returns:
        Extracted text content

    Raises:
        ValueError: If file format is not supported
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext not in EXTRACTORS:
        raise ValueError(f"Unsupported format: {ext}")

    return EXTRACTORS[ext](file_path)


__all__ = [
    "extract_text",
    "get_supported_extensions",
    "extract_pdf",
    "extract_docx",
    "extract_xlsx",
    "extract_csv",
    "extract_pptx",
]
