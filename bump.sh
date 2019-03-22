#!/bin/sh
set -e

scp workon cartbox@"$IP":
ssh cartbox@"$IP" '. workon && git pull && pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate'
