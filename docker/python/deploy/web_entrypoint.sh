#!/bin/sh
# For running migrations
echo " > Running migrations"
python manage.py migrate

exec "$@"
