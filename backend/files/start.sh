#!/bin/bash

pip install -r requirements.txt

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

# check if DJANGO_SETTINGS_MODULE is set to production or development
if [ "$DJANGO_SETTINGS_MODULE" = "backend.settings.development" ]; then
  # Delete all existing superusers and create a new one from .env file
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(is_superuser=True).delete()"
  python manage.py createsuperuser --noinput
fi

# Collect static files (needed for serving static files with daphne)
python manage.py collectstatic --noinput

# Start the ASGI server (Daphne in this case)
daphne -b 0.0.0.0 -p 8000 backend.asgi:application
# tail -f /dev/null