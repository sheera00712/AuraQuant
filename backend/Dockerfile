FROM python:3.11-slim

WORKDIR /app

# Install curl for health checks and ensure pip is available
RUN apt-get update && apt-get install -y curl && \
    python -m ensurepip --upgrade

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies using python -m pip to be explicit
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
