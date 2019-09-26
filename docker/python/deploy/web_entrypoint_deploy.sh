#!/bin/sh
# For running migrations
echo " > Run migrations (bash)"
python manage.py migrate


exec "$@"
