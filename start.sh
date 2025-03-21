#!/bin/bash

# Start SSH service in the background
/usr/sbin/sshd -D &

# Run Django database migrations
python manage.py migrate

# Start Django app with Gunicorn
gunicorn --bind 0.0.0.0:8000 orm1.wsgi:application
