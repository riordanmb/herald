#!/bin/bash
# Script to set up the database with migrations and initial data

set -e

echo "🗄️  Setting up Herald database..."

cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check if database is accessible
echo "📡 Checking database connection..."
python manage.py check --database default || {
    echo "❌ Database connection failed. Please ensure PostgreSQL is running."
    exit 1
}

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Checking for superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@herald.example.com', 'admin123')
    print("Superuser created: admin / admin123")
else:
    print("Superuser already exists")
EOF

# Seed initial data
echo "🌱 Seeding initial data..."
python manage.py seed_manuscripts --count 5 --user admin || {
    echo "⚠️  Seed script failed (this is optional)"
}

echo ""
echo "✅ Database setup complete!"
echo ""
echo "You can now:"
echo "  - Access admin at: http://localhost:8000/admin"
echo "  - Login with: admin / admin123"
echo "  - View API docs at: http://localhost:8000/api/docs"

