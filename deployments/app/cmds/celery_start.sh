#!/bin/bash
celery -A config.celery worker -l info