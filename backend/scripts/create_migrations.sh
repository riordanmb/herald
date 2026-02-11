#!/bin/bash
# Script to create database migrations

set -e

echo "🔄 Creating database migrations..."

cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Create migrations for all apps
python manage.py makemigrations manuscripts
python manage.py makemigrations authentication

echo "✅ Migrations created successfully!"
echo ""
echo "To apply migrations, run:"
echo "  python manage.py migrate"

