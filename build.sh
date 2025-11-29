#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "--- STARTING BUILD ---"

# 1. Force install Gunicorn and common tools directly
echo "Installing Gunicorn and basic tools..."
pip install --upgrade pip
pip install gunicorn
pip install whitenoise
pip install dj-database-url
pip install psycopg2-binary

# 2. Install the rest from requirements (if valid)
echo "Installing requirements from file..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "WARNING: requirements.txt not found!"
fi

# 3. Django setup
echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Applying migrations..."
python manage.py migrate

echo "--- CHECKING INSTALLED PACKAGES ---"
pip list | grep gunicorn
echo "--- BUILD FINISHED ---"