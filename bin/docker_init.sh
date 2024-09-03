#!/bin/bash

cd /blockadmin

python manage.py check >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo '--------------successfully configured!!!----------------'
    python manage.py migrate
    python manage.py collectstatic --noinput
    gunicorn -c python:blockadmin.gunicorn_conf blockadmin.wsgi -b 0.0.0.0:60000
else
    echo 'something went wrong.....'
    python manage.py check
fi
