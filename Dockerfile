FROM python:3.11-slim
COPY . .
RUN pip3 install nanobot-ai python-docx pymupdf
RUN mkdir -p /root/.nanobot/workspace/skills && \
    cp -r nanobot-config/skills/. /root/.nanobot/workspace/skills/
CMD ["nanobot", "gateway", "--config", "nanobot-config/config.json"]
