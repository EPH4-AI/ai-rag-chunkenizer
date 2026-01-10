"""
AI Chunkenizer - CSV Extractor
Text extraction from .csv files using pandas.

Copyright (c) 2025 VIEWVALUE LLC. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.
"""

import pandas as pd


def extract_csv(file_path: str) -> str:
    """
    Extract text from a CSV file.

    Converts CSV to markdown table format and includes
    basic statistics for numeric columns.

    Args:
        file_path: Path to the CSV file

    Returns:
        Text representation of the data

    Raises:
        Exception: If file cannot be parsed
    """
    try:
        # Read CSV with pandas
        df = pd.read_csv(
            file_path,
            encoding='utf-8',
            on_bad_lines='skip'
        )

        text_parts = ["[CSV Data]\n"]

        # Convert to markdown table
        text_parts.append(df.to_markdown(index=False))

        # Add summary for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            text_parts.append("\n\n[Statistics]")
            stats = df[numeric_cols].describe()
            text_parts.append(stats.to_markdown())

        return "\n\n".join(text_parts)

    except Exception as e:
        raise Exception(f"Failed to parse CSV: {str(e)}")
