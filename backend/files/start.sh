#!/bin/bash

wait_for_db() {
  echo "Waiting for database connection..."
  while ! nc -z db 5432; do
    sleep 1
  done
  echo "Database connected!"
}

cd backend/

wait_for_db

# # Run migrations (for example if the database is empty because of a new volume)
python manage.py migrate

# Delete all existing superusers
# python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(is_superuser=True).delete()"
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(is_superuser=True).delete()"

# Create the superuser from .env file
python manage.py createsuperuser --noinput

# Create an app
# python manage.py startapp custom_auth

# Create migrations for the app (only needed if a model is created or changed)
python manage.py makemigrations
python manage.py migrate

# Run the development server
# python manage.py runserver 0.0.0.0:8000

# Collect static files (needed for serving static files with daphne)
python manage.py collectstatic --noinput
# Start the ASGI server (Daphne in this case)
daphne -b 0.0.0.0 -p 8000 backend.asgi:application
# tail -f /dev/null
