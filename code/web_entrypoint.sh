#!/bin/sh
echo "dfslkjeofiljrioejfior"
python manage.py makemigrations
python manage.py migrate
exec "$@"
