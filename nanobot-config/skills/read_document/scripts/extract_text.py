#!/usr/bin/env python3
"""
extract_text.py — Extract text from .pdf, .docx, or .txt files.
Usage: python3 extract_text.py <file_path>
"""

import sys
from pathlib import Path


def extract_pdf(path: str) -> str:
    import fitz  # pymupdf
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)


def extract_docx(path: str) -> str:
    from docx import Document
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_txt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


EXTRACTORS = {
    ".pdf":  extract_pdf,
    ".docx": extract_docx,
    ".txt":  extract_txt,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_text.py <file_path>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    suffix = Path(path).suffix.lower()

    if suffix not in EXTRACTORS:
        print(f"Unsupported file type '{suffix}'. Supported: {', '.join(EXTRACTORS)}", file=sys.stderr)
        sys.exit(1)

    try:
        text = EXTRACTORS[suffix](path)
        print(text)
    except Exception as e:
        print(f"Error extracting text from {path}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
