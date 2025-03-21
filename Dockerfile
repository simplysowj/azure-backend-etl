FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy SSH configuration and application files
COPY sshd_config.txt /etc/ssh/sshd_config
COPY . .

# Copy start.sh and set it as executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose ports for Django and SSH
EXPOSE 8000 2222

# Start SSH and Django App
CMD ["/bin/bash", "/app/start.sh"]
