#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies from your fixed requirements file
pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate