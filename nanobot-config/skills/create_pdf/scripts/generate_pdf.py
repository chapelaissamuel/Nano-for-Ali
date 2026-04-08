#!/usr/bin/env python3
"""
generate_pdf.py — Generate a PDF from text content using fpdf2.

Usage:
  python3 generate_pdf.py "Text content here"
  echo "Text content" | python3 generate_pdf.py -

Output: prints the path to the generated PDF (/tmp/output.pdf).
"""

import sys
from fpdf import FPDF

OUTPUT_PATH = "/tmp/output.pdf"


def generate(text: str) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    for line in text.splitlines():
        pdf.multi_cell(0, 8, line if line.strip() else " ")

    pdf.output(OUTPUT_PATH)
    return OUTPUT_PATH


def main():
    if len(sys.argv) >= 2 and sys.argv[1] != "-":
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("Error: no content provided.", file=sys.stderr)
        sys.exit(1)

    path = generate(text)
    print(path)


if __name__ == "__main__":
    main()
