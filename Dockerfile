FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app
RUN echo $(ls -1 /app)

# Install Dependency from the builder
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "/app:/app/src:/opt/.local/bin:${PYTHONPATH}"
