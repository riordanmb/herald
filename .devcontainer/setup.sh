#!/bin/bash
set -e

echo "🚀 Setting up Herald development environment..."

# Install Node.js (required for frontend)
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y postgresql-client libpq-dev

# Set up backend
echo "🐍 Setting up Django backend..."
cd /workspace/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements/development.txt

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
until pg_isready -h localhost -p 5432 -U herald; do
  sleep 1
done

# Run migrations
echo "🔄 Running Django migrations..."
python manage.py migrate

# Create logs directory
mkdir -p logs

echo "✅ Backend setup complete!"

# Set up frontend
echo "⚛️  Setting up Next.js frontend..."
cd /workspace/frontend

# Install Node dependencies
npm install

echo "✅ Frontend setup complete!"

# Create start script
echo "📝 Creating start script..."
cat > /workspace/start.sh << 'SCRIPT'
#!/bin/bash

# Start backend
echo "🚀 Starting Django backend on port 8000..."
cd /workspace/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000 &

# Start frontend
echo "🚀 Starting Next.js frontend on port 3000..."
cd /workspace/frontend
npm run dev &

echo ""
echo "✅ Herald is running!"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000/api/v1/"
echo "📍 API Docs: http://localhost:8000/api/docs/"
echo "📍 Admin: http://localhost:8000/admin/"
echo ""
echo "To create a superuser, run:"
echo "  cd backend && source venv/bin/activate && python manage.py createsuperuser"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

wait
SCRIPT

chmod +x /workspace/start.sh

# Return to workspace root
cd /workspace

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start Herald, run:"
echo "  ./start.sh"
echo ""
echo "Or start services individually:"
echo "  Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "  Frontend: cd frontend && npm run dev"
echo ""
