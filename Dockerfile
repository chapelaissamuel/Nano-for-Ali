FROM python:3.11-slim
COPY . .
RUN apt-get update && apt-get install -y nodejs npm
RUN pip3 install nanobot-ai python-docx pymupdf fpdf2
RUN mkdir -p /root/.nanobot/workspace/skills && \
    cp -r nanobot-config/skills/. /root/.nanobot/workspace/skills/
CMD ["nanobot", "gateway", "--config", "nanobot-config/config.json"]
