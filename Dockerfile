# ARKHAM - Dockerized Test Environment
# Python 3.11 slim image for testing

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -s /bin/bash appuser

# Copy project files
COPY requirements.txt ./
COPY main.py ./
COPY arkam.py ./
COPY pytest.ini ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install test dependencies
RUN pip install --no-cache-dir pytest pytest-cov

# Create tests directory and copy test files
COPY tests/ ./tests/

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set Python path
ENV PYTHONPATH=/app

# Default command runs tests
CMD ["pytest", "-v", "--tb=short"]
