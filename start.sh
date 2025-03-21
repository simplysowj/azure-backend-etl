#!/bin/bash

# Start SSH service
/usr/sbin/sshd

# Start Django app with Gunicorn
gunicorn orm1.wsgi:application --bind 0.0.0.0:8000
