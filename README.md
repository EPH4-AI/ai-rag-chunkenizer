# AI Chunkenizer by EPH4™

**A product of VIEWVALUE LLC**

Fast, token-aware document chunking for RAG pipelines.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GDPR Compliant](https://img.shields.io/badge/GDPR-Compliant-green.svg)](#privacy--compliance)
[![SOC2 Compliant](https://img.shields.io/badge/SOC2-Compliant-green.svg)](#privacy--compliance)

## Features

- **Token-Aware Chunking** - Splits on word boundaries using tiktoken for accurate token counts
- **Multi-Format Support** - PDF, Word, Excel, CSV, PowerPoint
- **Fast Processing** - Optimized extractors (PyMuPDF for PDFs)
- **Configurable Overlap** - Maintain context between chunks
- **CLI & Python API** - Use from command line or import in your code
- **Browser Demo** - Try it without installing anything (100% client-side)

## Live Demo

Try it in your browser: [AI Chunkenizer Demo](https://eph4-ai.github.io/ai-chunkenizer)

> **Privacy Note:** The browser demo processes files entirely on your device. No data is uploaded, stored, or transmitted to any server.

---

## Privacy & Compliance

### How AI Chunkenizer Processes Your Files

#### Browser Demo - Step by Step Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ YOUR DEVICE (Everything happens here - nothing leaves)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Step 1: FILE SELECTION                                                     │
│  └── You click "Upload" or drag-drop a file                                 │
│  └── Browser's File API reads the file from YOUR disk                       │
│  └── File data goes into YOUR browser's memory (RAM)                        │
│                                                                             │
│  Step 2: TEXT EXTRACTION                                                    │
│  └── PDF files: PDF.js (Mozilla's library) parses the PDF locally           │
│  └── Word files: Mammoth.js extracts text locally                           │
│  └── Excel/CSV: SheetJS parses spreadsheet locally                          │
│  └── All libraries run as JavaScript in YOUR browser                        │
│  └── Zero HTTP requests made for your file data                             │
│                                                                             │
│  Step 3: CHUNKING                                                           │
│  └── JavaScript function splits text by word boundaries                     │
│  └── Token count estimated locally (chars ÷ 4)                              │
│  └── Chunks stored in JavaScript array in YOUR browser memory               │
│                                                                             │
│  Step 4: DISPLAY                                                            │
│  └── Results rendered as HTML in YOUR browser                               │
│  └── Download buttons use Blob API to create files locally                  │
│                                                                             │
│  Step 5: CLEANUP                                                            │
│  └── Close tab → Browser garbage collection clears all data                 │
│  └── Refresh page → All data gone                                           │
│  └── Nothing persisted to disk, server, or cloud                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ OUR SERVER (GitHub Pages - static file hosting only)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  What we serve: index.html, CSS, JavaScript code                            │
│  What we receive: NOTHING - no file data, no user data, no analytics        │
│  What we store: NOTHING - static hosting only                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Python Library - Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ YOUR MACHINE (Everything happens here)                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  $ ai-chunkenizer process document.pdf -o chunks.json                       │
│                                                                             │
│  1. Python reads file from YOUR local disk                                  │
│  2. PyMuPDF/python-docx/openpyxl extract text locally                       │
│  3. tiktoken counts tokens locally (no OpenAI API calls)                    │
│  4. Chunks saved to YOUR local disk                                         │
│                                                                             │
│  Network calls made: ZERO                                                   │
│  Data sent externally: NONE                                                 │
│  Telemetry/analytics: NONE                                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### GDPR Compliance - Specific Legal Basis

| GDPR Requirement | AI Chunkenizer Implementation |
|------------------|-------------------------------|
| **Article 4 (Processing)** | No processing occurs on our systems. All operations run on user's device. |
| **Article 6 (Lawful Basis)** | Not applicable - we don't process personal data. |
| **Article 13-14 (Information)** | Not applicable - no data collection to inform about. |
| **Article 17 (Right to Erasure)** | Automatic - closing browser tab erases all data. |
| **Article 24 (Controller)** | We are NOT a data controller - we never receive data. |
| **Article 25 (Privacy by Design)** | Architecture designed to make data collection impossible. |
| **Article 28 (Processor)** | We are NOT a data processor - we perform no processing. |
| **Article 32 (Security)** | No server-side data = no server-side security requirements. |
| **Article 33-34 (Breach Notification)** | Not applicable - no data to breach. |

**Legal Position:** Under GDPR, AI Chunkenizer (browser demo) is equivalent to a user opening a file in Notepad. The software runs locally, and we have no more access to the file than Microsoft has when you use Notepad.

### SOC2 Compliance - Specific Controls

| SOC2 Trust Principle | AI Chunkenizer Implementation |
|----------------------|-------------------------------|
| **Security** | No data in our possession = no data to secure. Client-side only. |
| **Availability** | Static HTML hosted on GitHub Pages. No server processing to fail. |
| **Processing Integrity** | All processing occurs client-side. We make no processing claims. |
| **Confidentiality** | Data never transmitted to us. Confidentiality maintained by architecture. |
| **Privacy** | Zero data collection. No personal information received or stored. |

**Technical Verification:** Users can verify compliance by:
1. Opening browser Developer Tools → Network tab
2. Processing a file
3. Observing zero HTTP requests containing file data
4. All requests are only for static assets (JS libraries, CSS)

### What This Means Legally

1. **We are not a "service provider"** under data protection law for the browser demo
2. **No Data Processing Agreement (DPA) needed** - we don't process your data
3. **No subprocessor concerns** - we don't send data anywhere
4. **No cross-border transfer issues** - data never leaves user's device
5. **No data retention policy needed** - we retain nothing

---

## Installation

```bash
pip install ai-chunkenizer
```

Or install from source:

```bash
git clone https://github.com/EPH4-AI/ai-chunkenizer.git
cd ai-chunkenizer
pip install -e .
```

## Quick Start

### Python API

```python
from chunkenizer import Chunkenizer

# Initialize with custom settings
chunker = Chunkenizer(max_tokens=1000, overlap_tokens=100)

# Process a document
result = chunker.process("annual_report.pdf")

print(f"Created {result.total_chunks} chunks")
print(f"Total tokens: {result.total_tokens}")

# Access chunks
for chunk in result.chunks:
    print(f"Chunk {chunk.index}: {chunk.token_count} tokens")
    print(chunk.text[:200])
```

### Command Line

```bash
# Process a single file
ai-chunkenizer process document.pdf -o chunks.json

# With custom settings
ai-chunkenizer process report.xlsx --max-tokens 500 --overlap 50

# Preview chunks
ai-chunkenizer process data.csv --preview 3

# Batch process a directory
ai-chunkenizer batch ./documents/ -o ./output/

# Show supported formats
ai-chunkenizer info
```

## Supported Formats

| Format | Extension | Engine |
|--------|-----------|--------|
| PDF | `.pdf` | PyMuPDF |
| Word | `.docx` | python-docx |
| Excel | `.xlsx`, `.xls` | openpyxl + pandas |
| CSV | `.csv` | pandas |
| PowerPoint | `.pptx` | python-pptx |

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_tokens` | 1000 | Maximum tokens per chunk |
| `overlap_tokens` | 100 | Tokens to overlap between chunks |
| `model` | "gpt-4" | Tokenizer model (for token counting) |

## Output Format

```json
{
  "source": "document.pdf",
  "total_chunks": 47,
  "total_tokens": 42350,
  "total_chars": 189420,
  "config": {
    "max_tokens": 1000,
    "overlap_tokens": 100
  },
  "chunks": [
    {
      "index": 0,
      "text": "This is the first chunk of text...",
      "token_count": 987,
      "char_count": 4521
    }
  ]
}
```

---

## Legal Disclaimer

### Limitation of Liability

THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

IN NO EVENT SHALL THE AUTHORS, COPYRIGHT HOLDERS, OR CONTRIBUTORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### AI Chunkenizer Specific Disclaimers

#### What AI Chunkenizer Does
- Extracts text from documents (PDF, DOCX, XLSX, CSV, PPTX)
- Splits text into smaller chunks based on token count
- Provides estimated token counts (not exact OpenAI token counts)
- Outputs chunks in various formats (JSON, TXT, CSV, HTML)

#### What AI Chunkenizer Does NOT Do
- Does NOT guarantee accurate token counts (estimation only: ~4 chars per token)
- Does NOT validate document contents for accuracy
- Does NOT scan for malware, viruses, or malicious content
- Does NOT encrypt, secure, or protect your files
- Does NOT provide legal, financial, or professional advice from extracted content
- Does NOT guarantee compatibility with any specific LLM or embedding model
- Does NOT guarantee identical results between browser and Python versions

#### No Responsibility for External Use

The authors and maintainers of AI Chunkenizer:

1. **Do not assume responsibility** for how third parties use, modify, or distribute this software
2. **Do not guarantee** the accuracy, completeness, or reliability of document processing results
3. **Do not provide** legal, compliance, or security advice through this software
4. **Are not liable** for any data loss, corruption, or security incidents arising from use of this software
5. **Do not warrant** that this software is suitable for any particular purpose, including but not limited to:
   - Processing of sensitive, confidential, or regulated data (HIPAA, PCI-DSS, financial data)
   - Legal or compliance document processing
   - Production or enterprise environments without proper evaluation
   - Any use case where chunking errors could cause harm

### User Responsibilities

By using AI Chunkenizer, you agree that:

1. **You are solely responsible** for evaluating whether this software meets your requirements
2. **You are solely responsible** for verifying the accuracy of chunking output before using in downstream applications
3. **You are solely responsible** for compliance with applicable laws and regulations in your jurisdiction
4. **You are solely responsible** for the security and handling of any data you process
5. **You must conduct your own security assessment** before using in production environments
6. **You must not use this software** for any illegal, harmful, or malicious purposes
7. **You understand** that token counts are estimates and may differ from actual LLM tokenization

### Third-Party Dependencies

AI Chunkenizer uses these third-party libraries, each with their own licenses:

| Library | License | Purpose |
|---------|---------|---------|
| PyMuPDF (fitz) | AGPL-3.0 | PDF extraction |
| python-docx | MIT | Word extraction |
| openpyxl | MIT | Excel extraction |
| pandas | BSD-3 | Data processing |
| python-pptx | MIT | PowerPoint extraction |
| tiktoken | MIT | Token counting |
| PDF.js | Apache-2.0 | Browser PDF parsing |
| Mammoth.js | BSD-2 | Browser DOCX parsing |
| SheetJS | Apache-2.0 | Browser spreadsheet parsing |

**Note on PyMuPDF:** PyMuPDF uses AGPL-3.0 license. If you use the Python library in your own software, review AGPL-3.0 requirements.

Users are responsible for reviewing and complying with all applicable third-party licenses.

### Indemnification

You agree to indemnify, defend, and hold harmless the authors, maintainers, and contributors of AI Chunkenizer from and against any claims, liabilities, damages, losses, and expenses arising from:
- Your use of this software
- Your violation of these terms
- Your violation of any third-party rights
- Any content you process using this software

---

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting a pull request.

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black chunkenizer/
ruff check chunkenizer/
```

## Want More?

This chunkenizer is the document processing engine behind **[EPH4](https://eph4.ai)** - our full AI document intelligence platform.

EPH4 adds:
- Automatic vector embeddings
- RAG-powered Q&A
- Intelligent chart generation
- Ephemeral secure sessions
- Zero setup required

[Try EPH4 Free](https://eph4.ai)

---

## License

MIT License - see [LICENSE](LICENSE) for details.

```
MIT License

Copyright (c) 2025 VIEWVALUE LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Trademarks

- **EPH4™** is a trademark of VIEWVALUE LLC

The MIT License grants rights to the software code only. It does not grant rights to use VIEWVALUE LLC trademarks. You may not use the name "EPH4" or VIEWVALUE LLC branding to endorse or promote products derived from this software without prior written permission.

---

**AI Chunkenizer** by **EPH4™** — A product of **VIEWVALUE LLC**
