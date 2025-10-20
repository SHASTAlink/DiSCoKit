# Use Python 3.12 slim image (matches development environment)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching optimization)
# When only code changes, this layer is cached and pip install is skipped
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from project directory
# Filtered by .dockerignore to exclude:
#   - .env files (secrets)
#   - data/ and logs/ (runtime files)
#   - venv/ and __pycache__/ (development files)
#   - .git/ (version control)
# Includes:
#   - app/ (application code)
#   - bot.py, wsgi.py, db_utils.py (Python modules)
#   - uwsgi.ini (if using uWSGI)
#   - docs/ (documentation - optional)
#   - experimental_conditions.json (or mount as volume)
COPY . .

# Create directories for mounted volumes
RUN mkdir -p /app/data /app/logs

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()"

# Run with Gunicorn (default)
# To use uWSGI instead: CMD ["uwsgi", "--ini", "uwsgi.ini"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:app"]
