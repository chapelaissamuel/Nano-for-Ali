#!/usr/bin/env python3
"""
generate_pdf.py — Generate a PDF and send it directly via Telegram Bot API.

Usage:
  python3 generate_pdf.py <chat_id> "Text content here"
  echo "Text content" | python3 generate_pdf.py <chat_id> -

Exit 0 = sent successfully. Exit 1 = failed (fallback message printed to stdout).
"""

import os
import sys
import json
import urllib.request
import urllib.error

from fpdf import FPDF

# nanobot's shell tool strips all env vars from subprocesses (security design).
# The token is written to /tmp/.tg_token by start.sh at container boot,
# before nanobot starts — this is the only reliable way to pass it.
TOKEN = ""
try:
    TOKEN = open("/tmp/.tg_token").read().strip()
except Exception:
    pass

# Fallback: env var (works when script is run directly, not via nanobot agent)
if not TOKEN:
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

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


def send_document(chat_id: str, file_path: str, token: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    boundary = "NanobotPDFBoundary"

    with open(file_path, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f"{chat_id}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="document"; filename="output.pdf"\r\n'
        f"Content-Type: application/pdf\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )

    # UNE SEULE tentative. Pas de retry. Telegram Flood Control prevention.
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read())
            print(f"Telegram error: {err.get('description', str(e))}", file=sys.stderr)
        except Exception:
            print(f"Telegram HTTP error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Network error: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_pdf.py <chat_id> [text... | -]", file=sys.stderr)
        sys.exit(1)

    chat_id = sys.argv[1]

    if len(sys.argv) >= 3 and sys.argv[2] != "-":
        text = " ".join(sys.argv[2:])
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("Error: no content provided.", file=sys.stderr)
        sys.exit(1)

    if not TOKEN:
        print("Error: token not found in /tmp/.tg_token or TELEGRAM_BOT_TOKEN env var.", file=sys.stderr)
        sys.exit(1)

    try:
        path = generate(text)
    except Exception as e:
        print(f"Je n'ai pas pu envoyer le PDF, voici le contenu :\n{text}")
        sys.exit(1)

    success = send_document(chat_id, path, TOKEN)

    if success:
        print("PDF envoyé ✅")
    else:
        print(f"Je n'ai pas pu envoyer le PDF, voici le contenu :\n{text}")
        sys.exit(1)


if __name__ == "__main__":
    main()
