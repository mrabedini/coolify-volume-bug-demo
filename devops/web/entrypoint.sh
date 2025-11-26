#!/bin/sh

# Create directories if they don't exist
mkdir -p /var/www/static /var/www/media

# Write initial test files
echo "Initialized at $(date)" > /var/www/static/init.txt
echo "Initialized at $(date)" > /var/www/media/init.txt

# Start the Flask application
python /app/app.py
