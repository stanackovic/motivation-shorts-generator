# Use official Python 3.9 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libasound2 \
    libffi-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libsndfile1 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install TTS moviepy Pillow requests

# Default command (adjust if needed)
CMD ["python", "main.py"]
