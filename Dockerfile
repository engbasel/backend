FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY flask_server/requirements.txt ./flask_server/
COPY ai_services/chatbot/requirements.txt ./ai_services/chatbot/
COPY ai_services/stroke_assessment/requirements.txt ./ai_services/stroke_assessment/
COPY ai_services/stroke_image/requirements.txt ./ai_services/stroke_image/

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r flask_server/requirements.txt && \
    pip install --no-cache-dir -r ai_services/chatbot/requirements.txt && \
    pip install --no-cache-dir -r ai_services/stroke_assessment/requirements.txt && \
    pip install --no-cache-dir -r ai_services/stroke_image/requirements.txt

COPY . .

RUN mkdir -p uploads uploads/scans

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "gateway.py"]