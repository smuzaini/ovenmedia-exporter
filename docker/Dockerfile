# Use official Python slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY src/ ./src/
COPY config/ ./config/

# Set PYTHONPATH so imports work correctly
ENV PYTHONPATH=/app/src

# Expose the metrics port
EXPOSE 8000

# Run the exporter
CMD ["python", "-m", "src.main"]
