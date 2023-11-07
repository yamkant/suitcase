#!/bin/sh

poetry run celery -A config worker -l info