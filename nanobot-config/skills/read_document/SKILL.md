---
name: read_document
description: Read and extract text from .docx, .pdf, and .txt files sent via Telegram.
metadata: {"nanobot":{"emoji":"📄","requires":{"bins":["python3"]}}}
---

# Read Document

Extract and analyse the content of documents sent by the user (.docx, .pdf, .txt).

## When to use

Use this skill immediately when the user sends a file attachment or asks you to read/analyse a document.

## How to extract text

Use the helper script at `/app/nanobot-config/skills/read_document/scripts/extract_text.py`.

```bash
python3 /app/nanobot-config/skills/read_document/scripts/extract_text.py /path/to/file.pdf
```

The script auto-detects the file type and prints extracted text to stdout.

### Manual extraction (fallback)

**PDF** (via pymupdf):
```python
import fitz
doc = fitz.open("/path/to/file.pdf")
text = "\n".join(page.get_text() for page in doc)
print(text)
```

**DOCX** (via python-docx):
```python
from docx import Document
doc = Document("/path/to/file.docx")
text = "\n".join(p.text for p in doc.paragraphs)
print(text)
```

**TXT**:
```python
text = open("/path/to/file.txt", encoding="utf-8").read()
print(text)
```

## Workflow

1. The file arrives as a Telegram attachment — nanobot saves it to a temp path.
2. Run the extract script on that path.
3. Read the extracted text and answer the user's question about it.
4. If the document is very long (>10 000 chars), summarise the key points first, then offer to go deeper on any section.

## Tips

- Always confirm what file was received before extracting.
- If extraction fails, report the error clearly and suggest the user send the file as plain `.txt`.
- Respect the response-style skill: keep answers concise, split if long.
