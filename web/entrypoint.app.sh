#!/bin/sh

cd apps/
poetry run python manage.py migrate
poetry run python manage.py migrate django_celery_results
poetry run python manage.py createcachetable

poetry run python manage.py runserver 0.0.0.0:8000