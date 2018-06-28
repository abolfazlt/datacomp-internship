#!/usr/bin/env bash

# Change Environment
workon datacomp

# Prepare db schema
python manage.py migrate --noinput

# Prepare log files and start outputting logs to stdout
mkdir logs/
touch logs/gunicorn.log
touch logs/access.log
tail -n 0 -f logs/*.log &

# Start gunicorn processes
exec gunicorn datacomp.wsgi:application \
    --name datacomp-gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 33 \
    --log-level=info \
    --log-file=logs/gunicorn.log \
    --access-logfile=logs/access.log \
    --timeout 3000 \
    --reload \
    --daemon
