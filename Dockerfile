FROM python:3.11-slim
COPY . .
RUN pip3 install nanobot-ai python-docx pymupdf
CMD ["nanobot", "gateway", "--config", "nanobot-config/config.json"]
