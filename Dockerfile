FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN find / -name generate_pdf.py 2>/dev/null && \
    ls -la /app/nanobot-config/skills/create_pdf/scripts/
RUN mkdir -p /app/nanobot-config/skills/create_pdf/scripts
RUN apt-get update && apt-get install -y nodejs npm
RUN pip3 install nanobot-ai python-docx pymupdf fpdf2
RUN mkdir -p /root/.nanobot/workspace/skills && \
    cp -r nanobot-config/skills/. /root/.nanobot/workspace/skills/
CMD ["/bin/bash", "/app/nanobot-config/start.sh"]
