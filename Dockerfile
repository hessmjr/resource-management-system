# Use Python 3.12 Alpine for smaller, more secure image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-connector-c-dev \
    pkgconfig

# Install uv for fast dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./
COPY requirements.txt ./

# Install dependencies using uv
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser -D -s /bin/sh appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000')" || exit 1

# Run application
CMD ["python", "src/main.py"]
