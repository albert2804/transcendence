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

# Create migrations for the app (only needed if a model is created or changed)
python manage.py makemigrations
python manage.py migrate

# Delete all existing superusers
# python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(is_superuser=True).delete()"
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(is_superuser=True).delete()"

# Create the superuser from .env file
python manage.py createsuperuser --noinput

#create test user
python manage.py createsuperuser --noinput --username=johndoe
python manage.py createsuperuser --noinput --username=johndoe2
python manage.py createsuperuser --noinput --username=johndoe3
python manage.py createsuperuser --noinput --username=pnolte
python manage.py createsuperuser --noinput --username=albert
python manage.py createsuperuser --noinput --username=kathrin
python manage.py createsuperuser --noinput --username=kekse
python manage.py createsuperuser --noinput --username=kek
python manage.py createsuperuser --noinput --username=nikkka
python manage.py createsuperuser --noinput --username=stephanie

# Collect static files (needed for serving static files with daphne)
python manage.py collectstatic --noinput

# Start the ASGI server (Daphne in this case)
# daphne -b 0.0.0.0 -p 8000 backend.asgi:application

tail -f /dev/null



# Create an app
# python manage.py startapp custom_auth
