#!/bin/sh

cd apps/

poetry run celery -A config worker -l info