#!/bin/bash
python manage.py createsuperuser --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL" \
    --phone_number "$DJANGO_SUPERUSER_PHONE_NUMBER"

echo "Starting server..."
exec "$@"
