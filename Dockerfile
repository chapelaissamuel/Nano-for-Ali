FROM python:3.11-slim
COPY . .
RUN pip3 install nanobot-ai
CMD ["bash", "nanobot-config/start.sh"]
