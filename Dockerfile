FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip3 install -e nanobot/

CMD ["bash", "nanobot-config/start.sh"]
