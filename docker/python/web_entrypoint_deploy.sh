#!/bin/sh
# For running migrations
echo " > Run migrations (bash)"
python manage.py migrate


# For creating admin
echo " > Create admin (bash)"

MAIL=$SUPERUSER_USERNAME
PASS=$SUPERUSER_PASSWORD
script="
from django.contrib.auth import get_user_model;
User = get_user_model();

email = '$MAIL';
password = '$PASS';

if User.objects.filter(email=email).count()==0:
    User.objects.create_superuser(email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped, user exists.');
"
printf "$script" | python manage.py shell


exec "$@"
