FROM python:3.11-slim

# Set workdir
WORKDIR /app

# System deps (optional but useful for psycopg etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY src ./src

# Set PYTHONPATH so "text_ingestion" is importable
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Default port for Cloud Run
ENV PORT=8080

# Command: run FastAPI via Uvicorn
CMD ["uvicorn", "text_ingestion.main:app", "--host", "0.0.0.0", "--port", "8080"]
