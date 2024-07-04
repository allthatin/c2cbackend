#!/bin/bash

# run cron
echo "$(env ; crontab -l)" | crontab - 
/etc/init.d/cron start
python manage.py crontab add

# gunicorn
PYTHONWARNINGS="ignore" /usr/local/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8000 --chdir=/app/backend --log-level debug --error-logfile - --access-logfile - --capture-output --reload