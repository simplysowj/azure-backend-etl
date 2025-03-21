# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies including SSH
RUN apt-get update && apt-get install -y \
    openssh-server \
    build-essential \
    libpq-dev \
    gcc \
    curl && \
    rm -rf /var/lib/apt/lists/*  # Clean up apt cache

# Set up SSH configuration
RUN mkdir /var/run/sshd && \
    echo 'root:Docker!' | chpasswd && \
    chmod 600 /etc/ssh/sshd_config

# Copy SSH configuration file
COPY sshd_config.txt /etc/ssh/sshd_config

# Copy application files
COPY . .

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose ports for Django and SSH
EXPOSE 8000 2222

# Start SSH and Django App
CMD ["/app/start.sh"]
