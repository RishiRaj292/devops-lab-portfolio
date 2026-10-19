# Official lightweight Python base image
FROM python:3.9-slim

WORKDIR /app

# Install ping and curl utilities for networking connectivity tests
RUN apt-get update && apt-get install -y iputils-ping curl && rm -rf /var/lib/apt/lists/*

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port
EXPOSE 5001

# Start Flask API server
CMD ["python", "app.py"]
