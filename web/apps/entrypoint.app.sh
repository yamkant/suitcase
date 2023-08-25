#!/bin/sh

python3 -m pip install --upgrade pip
pip install -r requirements.txt

python3 manage.py migrate

# gunicorn --bind 0.0.0.0:8000 config.wsgi:application
python3 /apps/manage.py runserver 0.0.0.0:8000

