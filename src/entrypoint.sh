#!/bin/sh

set -e

/wait

echo start_entrypoint
python manage.py collectstatic --no-input --clear
#python manage.py wait_for_db
python manage.py makemigrations
python manage.py migrate
echo end_entrypoint

exec "$@"