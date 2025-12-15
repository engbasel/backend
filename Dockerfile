FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy all requirements files first (for better caching)
COPY requirements.txt .
COPY flask_server/requirements.txt ./flask_server/
COPY ai_services/chatbot/requirements.txt ./ai_services/chatbot/
COPY ai_services/stroke_assessment/requirements.txt ./ai_services/stroke_assessment/
COPY ai_services/stroke_image/requirements.txt ./ai_services/stroke_image/

# Install all Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r flask_server/requirements.txt && \
    pip install --no-cache-dir -r ai_services/chatbot/requirements.txt && \
    pip install --no-cache-dir -r ai_services/stroke_assessment/requirements.txt && \
    pip install --no-cache-dir -r ai_services/stroke_image/requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p uploads uploads/scans

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command (can be overridden in docker-compose)
CMD ["python", "gateway.py"]