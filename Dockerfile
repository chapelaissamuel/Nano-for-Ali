FROM python:3.11-slim
COPY . .
RUN pip3 install nanobot-ai
CMD ["nanobot", "gateway", "--config", "nanobot-config/config.json"]
