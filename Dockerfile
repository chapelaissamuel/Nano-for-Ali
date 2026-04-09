FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    bubblewrap nodejs npm && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir nanobot-ai fpdf2 python-docx pymupdf

COPY nanobot-config/ nanobot-config/

RUN mkdir -p /root/.nanobot/workspace/skills && \
    cp -r nanobot-config/skills/. /root/.nanobot/workspace/skills/

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["gateway", "--config", "/app/nanobot-config/config.json"]
