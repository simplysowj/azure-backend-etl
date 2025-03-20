# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    openssh-server && \
    rm -rf /var/lib/apt/lists/*  # Clean up apt cache

# Set up SSH
RUN mkdir /var/run/sshd && \
    echo 'root:Docker!' | chpasswd && \
    echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config && \
    echo 'export VISIBLE=now' >> /etc/profile

# Install pipenv or requirements.txt dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files into the container
COPY . .

# Collect static files (optional, for production)
# RUN python manage.py collectstatic --noinput

# Expose ports (on separate lines, but without comments)
EXPOSE 8000
EXPOSE 2222

# Run migrations, start SSH, and run the app
CMD service ssh start && python manage.py migrate && gunicorn orm1.wsgi:application --bind 0.0.0.0:8000
