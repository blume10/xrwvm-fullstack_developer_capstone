#!/bin/sh
# ------------------------------------------
# Initialisiert die Django-Datenbank im Container
# ------------------------------------------

echo "📦 Making migrations and migrating the database..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Starte dann den übergebenen Befehl (CMD aus Dockerfile)
exec "$@"
