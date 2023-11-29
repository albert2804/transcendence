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
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(is_superuser=True).delete()"

# Create the superuser from .env file
python manage.py createsuperuser --noinput

# Run the development server
python manage.py runserver 0.0.0.0:8000

# for production-server we can use for example gunicorn
# but we need to add gunicorn to requirements.txt ;)
# gunicorn --bind 0.0.0.0:8000 backend.wsgi:application

