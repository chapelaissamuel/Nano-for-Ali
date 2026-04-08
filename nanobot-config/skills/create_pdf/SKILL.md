---
name: create_pdf
description: Generate a PDF from text content and send it to the user via Telegram.
metadata: {"nanobot":{"emoji":"📝","requires":{"bins":["python3"]}}}
---

# Create PDF

Generate a PDF file from text content and deliver it directly to the user via the Telegram Bot API.

## When to use

Use this skill when the user asks to:
- Create a PDF
- Send something as a PDF
- Export content to PDF

## How to generate and send the PDF

You need the user's `chat_id` (available from the conversation context) and the text content.

```bash
python3 /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py "<chat_id>" "Full text content here"
```

Or pipe long content:

```bash
echo "Your text content" | python3 /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py "<chat_id>" -
```

The script:
1. Generates a PDF at `/tmp/output.pdf` using fpdf2
2. Sends it to the user via `https://api.telegram.org/bot.../sendDocument` (multipart/form-data)
3. Exits 0 and prints `PDF envoyé ✅` on success
4. Exits 1 and prints the fallback message on failure

## Critical Rules

- NEVER say the PDF was sent if the script exits with code 1 or prints an error.
- If the script outputs `Je n'ai pas pu envoyer le PDF, voici le contenu :`, relay that message verbatim to the user followed by the text content.
- NEVER claim the file exists if the script errored during PDF generation.
- Only confirm success when the script outputs `PDF envoyé ✅`.
