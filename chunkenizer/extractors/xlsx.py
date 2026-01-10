"""
AI Chunkenizer - Excel Extractor
Text extraction from .xlsx files using openpyxl and pandas.

Copyright (c) 2025 VIEWVALUE LLC. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.
"""

import openpyxl
import pandas as pd
from io import BytesIO
from pathlib import Path


def extract_xlsx(file_path: str) -> str:
    """
    Extract text from an Excel file.

    Each sheet is converted to a markdown-style table format
    for optimal text representation.

    Args:
        file_path: Path to the .xlsx file

    Returns:
        Text representation of all sheets

    Raises:
        Exception: If file cannot be processed
    """
    try:
        # Load workbook with data_only=True to get values instead of formulas
        wb = openpyxl.load_workbook(file_path, data_only=True)
        text_parts = []

        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]

            # Convert to DataFrame
            data = list(sheet.values)
            if not data:
                continue

            # First row as headers
            headers = data[0] if data else None
            rows = data[1:] if len(data) > 1 else []

            if not headers:
                continue

            df = pd.DataFrame(rows, columns=headers)

            # Clean up empty rows/columns
            df = df.dropna(how='all').dropna(axis=1, how='all')

            if df.empty:
                continue

            # Convert to markdown table
            sheet_text = f"[Sheet: {sheet_name}]\n\n"
            sheet_text += df.to_markdown(index=False)
            text_parts.append(sheet_text)

        wb.close()

        return "\n\n".join(text_parts)

    except Exception as e:
        raise Exception(f"Failed to extract Excel file: {str(e)}")
