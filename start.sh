#!/bin/bash

echo "🚀 Starting Herald..."
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the Herald root directory"
    exit 1
fi

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Backend virtual environment not found!"
    echo "Please run the setup first:"
    echo "  cd backend"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements/development.txt"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not installed!"
    echo "Please run:"
    echo "  cd frontend"
    echo "  npm install"
    exit 1
fi

# Start backend
echo "🐍 Starting Django backend on port 8000..."
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Give backend a moment to start
sleep 2

# Start frontend
echo "⚛️  Starting Next.js frontend on port 3000..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait a moment for services to start
sleep 3

echo ""
echo "✅ Herald is running!"
echo ""
echo "📍 Services:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000/api/v1/"
echo "   API Docs:  http://localhost:8000/api/docs/"
echo "   Admin:     http://localhost:8000/admin/"
echo ""
echo "📋 Process IDs:"
echo "   Backend:  $BACKEND_PID"
echo "   Frontend: $FRONTEND_PID"
echo ""
echo "📄 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop services:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   Or: pkill -f 'manage.py runserver'"
echo "   Or: pkill -f 'next dev'"
echo ""
echo "💡 To create a superuser:"
echo "   cd backend && source venv/bin/activate && python manage.py createsuperuser"
echo ""
echo "Press Ctrl+C to view this menu again (services will keep running in background)"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Services are still running in the background."
    echo "To stop them, run: kill $BACKEND_PID $FRONTEND_PID"
    exit 0
}

trap cleanup INT

# Keep script running to show status
wait
