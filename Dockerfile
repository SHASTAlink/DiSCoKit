# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY bot.py .
COPY experimental_conditions.json .
COPY wsgi.py .

# Create necessary directories
RUN mkdir -p data logs app/static/images

# Copy static images if they exist (won't fail if missing)
COPY app/static/images/* ./app/static/images/ 2>/dev/null || true

# Set permissions
RUN chmod -R 755 /app && \
    chmod -R 777 data logs

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()" || exit 1

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "120", "--access-logfile", "logs/access.log", "--error-logfile", "logs/error.log", "--log-level", "info", "wsgi:app"]