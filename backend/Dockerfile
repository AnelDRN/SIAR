# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies for GDAL
RUN apt-get update && apt-get install -y --no-install-recommends gdal-bin libgdal-dev build-essential

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly copy the analysis data to ensure it's available
COPY analysis/data /app/analysis/data

# Copy project
COPY . .
