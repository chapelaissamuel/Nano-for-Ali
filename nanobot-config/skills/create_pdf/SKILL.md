---
name: create_pdf
description: Generate a PDF from text content and send it to the user via Telegram.
metadata: {"nanobot":{"emoji":"📝","requires":{"bins":["python3"]}}}
---

# Create PDF

Generate a PDF file from text content and deliver it to the user.

## When to use

Use this skill when the user asks to:
- Create a PDF
- Send something as a PDF
- Export content to PDF

## How to generate the PDF

Run the helper script with the text content as an argument:

```bash
python3 /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py "Your full text content here"
```

Or pipe content into it:

```bash
echo "Your text content" | python3 /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py -
```

The script saves the PDF to `/tmp/output.pdf` and prints that path to stdout.

## Workflow

1. Generate the text content based on the user's request.
2. Run `generate_pdf.py` with that content.
3. Send `/tmp/output.pdf` to the user via Telegram's send_document function.
4. Confirm only if the send succeeds. If it fails, say exactly: "Je n'ai pas pu envoyer le fichier. Voici le contenu directement ici : [contenu]"

## Critical Rules

- NEVER say the PDF was sent if the send failed or returned an error.
- NEVER claim the file exists if the script errored.
- If `generate_pdf.py` fails, report the error in one sentence and paste the content as plain text instead.
