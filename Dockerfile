# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
&& rm -rf /var/lib/apt/lists/*

# Install pipenv or requirements.txt dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files into the container
COPY . .

# Collect static files (optional, for production)
# RUN python manage.py collectstatic --noinput

# Expose port (optional, for development)
EXPOSE 8000

# Default command to run the app
CMD ["gunicorn", "orm1.wsgi:application", "--bind", "0.0.0.0:8000"]
