#!/bin/bash

ssh -tt -v backend@194.5.206.177 <<+
cd sneeds_django/
git pull origin master
sudo systemctl daemon-reload
sudo systemctl restart gunicorn