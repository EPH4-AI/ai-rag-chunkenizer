"""
AI RAG Chunkenizer - Command Line Interface
Process documents from the terminal.
A product of EPH4™ by VIEWVALUE LLC.

Copyright (c) 2025 VIEWVALUE LLC. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.

EPH4™ is a trademark of VIEWVALUE LLC.

PRIVACY NOTICE:
    This CLI tool processes files entirely on your local machine.
    No data is uploaded, transmitted, or shared with any external service.
    No telemetry or usage analytics are collected.
"""

import json
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from .core import Chunkenizer

app = typer.Typer(
    name="ai-rag-chunkenizer",
    help="Fast, token-aware document chunking for RAG pipelines.",
    add_completion=False,
)
console = Console()


@app.command()
def process(
    file_path: str = typer.Argument(..., help="Path to document file"),
    output: Optional[str] = typer.Option(None, "-o", "--output", help="Output JSON file"),
    max_tokens: int = typer.Option(1000, "-m", "--max-tokens", help="Max tokens per chunk"),
    overlap: int = typer.Option(100, "-l", "--overlap", help="Overlap tokens between chunks"),
    preview: int = typer.Option(0, "-p", "--preview", help="Preview first N chunks"),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Minimal output"),
):
    """
    Process a document and split into chunks.

    Supports: PDF, DOCX, XLSX, CSV, PPTX
    """
    path = Path(file_path)

    if not path.exists():
        console.print(f"[red]Error:[/red] File not found: {file_path}")
        raise typer.Exit(1)

    chunker = Chunkenizer(max_tokens=max_tokens, overlap_tokens=overlap)

    # Check if format is supported
    if path.suffix.lower() not in chunker.SUPPORTED_EXTENSIONS:
        console.print(f"[red]Error:[/red] Unsupported format: {path.suffix}")
        console.print(f"Supported: {', '.join(chunker.SUPPORTED_EXTENSIONS)}")
        raise typer.Exit(1)

    if not quiet:
        console.print(Panel.fit(
            f"[bold blue]AI RAG Chunkenizer[/bold blue]\n"
            f"Processing: {path.name}",
            border_style="blue"
        ))

    # Process with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        disable=quiet,
    ) as progress:
        progress.add_task("Extracting and chunking...", total=None)
        result = chunker.process(file_path)

    if not quiet:
        # Display summary table
        table = Table(title="Chunking Results", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Source", result.source)
        table.add_row("Total Chunks", str(result.total_chunks))
        table.add_row("Total Tokens", f"{result.total_tokens:,}")
        table.add_row("Total Characters", f"{result.total_chars:,}")
        table.add_row("Avg Tokens/Chunk", f"{result.total_tokens // max(1, result.total_chunks):,}")

        console.print(table)

    # Preview chunks if requested
    if preview > 0 and not quiet:
        console.print(f"\n[bold]Preview (first {min(preview, result.total_chunks)} chunks):[/bold]\n")
        for chunk in result.chunks[:preview]:
            preview_text = chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text
            console.print(Panel(
                preview_text,
                title=f"Chunk {chunk.index + 1} ({chunk.token_count} tokens)",
                border_style="dim"
            ))

    # Output to file
    if output:
        output_path = Path(output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

        if not quiet:
            console.print(f"\n[green]Saved to:[/green] {output_path}")
    elif quiet:
        # In quiet mode with no output, print JSON to stdout
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


@app.command()
def batch(
    directory: str = typer.Argument(..., help="Directory containing documents"),
    output_dir: Optional[str] = typer.Option(None, "-o", "--output", help="Output directory"),
    max_tokens: int = typer.Option(1000, "-m", "--max-tokens", help="Max tokens per chunk"),
    overlap: int = typer.Option(100, "-l", "--overlap", help="Overlap tokens"),
    pattern: str = typer.Option("*", "-g", "--glob", help="File pattern to match"),
):
    """
    Batch process multiple documents in a directory.
    """
    dir_path = Path(directory)

    if not dir_path.is_dir():
        console.print(f"[red]Error:[/red] Not a directory: {directory}")
        raise typer.Exit(1)

    chunker = Chunkenizer(max_tokens=max_tokens, overlap_tokens=overlap)

    # Find matching files
    files = [
        f for f in dir_path.glob(pattern)
        if f.suffix.lower() in chunker.SUPPORTED_EXTENSIONS
    ]

    if not files:
        console.print("[yellow]No supported files found.[/yellow]")
        raise typer.Exit(0)

    console.print(f"[bold]Found {len(files)} files to process[/bold]\n")

    # Create output directory if specified
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

    # Process each file
    results_summary = []

    with Progress(console=console) as progress:
        task = progress.add_task("Processing files...", total=len(files))

        for file_path in files:
            try:
                result = chunker.process(str(file_path))
                results_summary.append({
                    "file": file_path.name,
                    "chunks": result.total_chunks,
                    "tokens": result.total_tokens,
                    "status": "success"
                })

                # Save if output directory specified
                if output_dir:
                    out_file = out_path / f"{file_path.stem}.json"
                    with open(out_file, "w", encoding="utf-8") as f:
                        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

            except Exception as e:
                results_summary.append({
                    "file": file_path.name,
                    "chunks": 0,
                    "tokens": 0,
                    "status": f"error: {str(e)[:50]}"
                })

            progress.advance(task)

    # Summary table
    table = Table(title="Batch Processing Results")
    table.add_column("File", style="cyan")
    table.add_column("Chunks", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("Status")

    for r in results_summary:
        status_style = "green" if r["status"] == "success" else "red"
        table.add_row(
            r["file"],
            str(r["chunks"]),
            f"{r['tokens']:,}",
            f"[{status_style}]{r['status']}[/{status_style}]"
        )

    console.print(table)


@app.command()
def info():
    """
    Show supported file formats and configuration options.
    """
    console.print(Panel.fit(
        "[bold blue]AI RAG Chunkenizer[/bold blue]\n"
        "Fast, token-aware document chunking for RAG pipelines",
        border_style="blue"
    ))

    console.print("\n[bold]Supported Formats:[/bold]")
    formats = [
        (".pdf", "PDF documents", "PyMuPDF"),
        (".docx", "Word documents", "python-docx"),
        (".xlsx/.xls", "Excel spreadsheets", "openpyxl + pandas"),
        (".csv", "CSV files", "pandas"),
        (".pptx", "PowerPoint presentations", "python-pptx"),
    ]

    table = Table(show_header=True)
    table.add_column("Extension", style="cyan")
    table.add_column("Description")
    table.add_column("Engine", style="dim")

    for ext, desc, engine in formats:
        table.add_row(ext, desc, engine)

    console.print(table)

    console.print("\n[bold]Default Configuration:[/bold]")
    console.print("  Max tokens per chunk: 1000")
    console.print("  Overlap tokens: 100")
    console.print("  Tokenizer: tiktoken (GPT-4)")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
