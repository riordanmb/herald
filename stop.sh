#!/bin/bash

echo "🛑 Stopping Herald services..."

# Stop Django
pkill -f "manage.py runserver" && echo "✅ Django stopped" || echo "ℹ️  Django not running"

# Stop Next.js
pkill -f "next dev" && echo "✅ Next.js stopped" || echo "ℹ️  Next.js not running"

# Clean up log files
rm -f backend.log frontend.log 2>/dev/null

echo ""
echo "✅ All services stopped"
