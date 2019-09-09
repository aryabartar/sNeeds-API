#!/bin/sh
# For running migrations
echo " > Run migrations"
python manage.py migrate



# For creating admin
echo " > Create admin"

MAIL="a@g.com"
PASS="111111"
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
