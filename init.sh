#!/bin/bash
# Railway initialization script

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py create_admin

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Database initialized!"
