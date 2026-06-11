# Use official slim Python runtime as base image 
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing byte-code .pyc out 
ENV PYTHONDONTWRITEBYTECODE=1
# Force Python output logs to directly pipe to stdout unbuffered
ENV PYTHONUNBUFFERED=1

# Install system dependencies (C-compilers / image processors)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Leverage Docker cache mapping requirements independently first
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all application contents to WORKDIR
COPY . .

# Expose internal router port
EXPOSE 8000

# Start execution entry point
# Use a single worker logic initially since this model runs synchronously PyTorch
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
