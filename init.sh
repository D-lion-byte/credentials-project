#!/bin/bash
# Railway initialization script

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Database initialized!"
