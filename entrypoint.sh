#!/bin/sh

# Exit immediately if a command fails
set -e

# Run Django migrations
echo "Running migrations..."
python manage.py migrate

# Create a superuser if not exists
echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('manoharreddy', 'lakshmimanohart@gmail.com', 'reddy')
"

# Start the server
echo "Starting server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000