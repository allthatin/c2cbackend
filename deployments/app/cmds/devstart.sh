#!/bin/bash

# gunicorn
PYTHONWARNINGS="ignore" /usr/local/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8001 --chdir=/app/backend --log-level debug --error-logfile - --access-logfile - --capture-output --reload