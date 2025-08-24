#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='manoharreddy').exists():
    User.objects.create_superuser('syko_reddy', 'lakshmimanohart@gmail.com', 'reddy2005')
else:
    print('Superuser already exists.')
"

echo "Starting server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000