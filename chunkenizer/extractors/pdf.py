"""
AI Chunkenizer - PDF Extractor
Text extraction using PyMuPDF (fitz).

Copyright (c) 2025 VIEWVALUE LLC. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.

NOTE: PyMuPDF uses AGPL-3.0 license. Review AGPL requirements if
incorporating this into your own distributed software.

PyMuPDF is chosen for its speed - significantly faster than alternatives
like pdfplumber or PyPDF2 for text extraction.
"""

import fitz  # PyMuPDF


def extract_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.

    Uses PyMuPDF for fast, reliable text extraction.
    Processes all pages sequentially and combines text.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text from all pages

    Raises:
        Exception: If PDF cannot be opened or processed
    """
    try:
        doc = fitz.open(file_path)
        text_parts = []

        for page_num, page in enumerate(doc, 1):
            page_text = page.get_text()
            if page_text.strip():
                text_parts.append(f"[Page {page_num}]\n{page_text}")

        doc.close()

        return "\n\n".join(text_parts)

    except Exception as e:
        raise Exception(f"Failed to extract PDF: {str(e)}")
