# Herald - GitHub Codespaces Setup

This directory contains the configuration for running Herald in GitHub Codespaces.

## What Gets Set Up

When you open this repository in Codespaces, the following happens automatically:

### Services Started
- **PostgreSQL 16** - Database on port 5432
- **Redis 7** - Cache on port 6379
- **MinIO** - Object storage on ports 9000 (API) and 9001 (Console)

### Backend (Django)
- Python 3.11 virtual environment
- All dependencies installed
- Database migrations run
- Django development server ready on port 8000

### Frontend (Next.js)
- Node.js 20
- All npm dependencies installed
- Next.js development server ready on port 3000

### VS Code Extensions
- Python support (Pylance, Black formatter)
- JavaScript/TypeScript support
- Tailwind CSS IntelliSense
- ESLint & Prettier
- Docker support

## Quick Start

Once your Codespace is created (takes 2-3 minutes):

### 1. Start Everything at Once

```bash
./start.sh
```

This starts both backend and frontend. You'll see:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/v1/
- API Docs: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

### 2. Create a Superuser (for Django Admin)

In a new terminal:

```bash
cd backend
source venv/bin/activate
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 3. Access the Application

Click on the "Ports" tab in VS Code and click the globe icon next to port 3000 to open Herald in your browser.

## Manual Start (Alternative)

If you prefer to start services separately:

### Backend Only
```bash
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### Frontend Only
```bash
cd frontend
npm run dev
```

## Accessing Services

### Frontend (Next.js)
- URL: Port 3000
- The main Herald application interface

### Backend API (Django)
- URL: Port 8000
- API Root: `/api/v1/`
- Interactive API Docs: `/api/docs/`
- Admin Interface: `/admin/` (requires superuser)

### Database (PostgreSQL)
- Host: localhost
- Port: 5432
- Database: herald
- User: herald
- Password: herald_dev_password

### Object Storage (MinIO)
- API: Port 9000
- Console: Port 9001
- Access Key: minioadmin
- Secret Key: minioadmin

## Common Tasks

### Run Django Management Commands
```bash
cd backend
source venv/bin/activate
python manage.py <command>
```

### Access Django Shell
```bash
cd backend
source venv/bin/activate
python manage.py shell
```

### Run Tests
```bash
# Backend tests
cd backend
source venv/bin/activate
pytest

# Frontend tests
cd frontend
npm test
```

### View Logs
Backend and frontend logs appear in the terminal where you ran `./start.sh`

## Troubleshooting

### Port Already in Use
If you see "port already in use", kill existing processes:
```bash
pkill -f "manage.py runserver"
pkill -f "next dev"
```

### Database Connection Issues
Check if PostgreSQL is running:
```bash
pg_isready -h localhost -p 5432 -U herald
```

### Reset Everything
Stop all services (Ctrl+C) and rebuild the Codespace:
- Go to Codespace settings (gear icon)
- Select "Rebuild Container"

## File Structure

```
.devcontainer/
├── devcontainer.json      # Main configuration
├── docker-compose.yml     # Services (PostgreSQL, Redis, MinIO)
├── setup.sh              # Post-create setup script
└── README.md             # This file
```

## Performance Tips

- Codespaces provides 2-4 cores and 8GB RAM by default
- Hot reload works for both backend and frontend
- Changes are automatically synced
- Use the integrated terminal for best performance

## Stopping Services

Press `Ctrl+C` in the terminal where `./start.sh` is running.

Or kill individual processes:
```bash
# Find processes
ps aux | grep "manage.py\|next"

# Kill by PID
kill <PID>
```

## Need Help?

- Check the main [README.md](../README.md)
- Review [GETTING_STARTED.md](../GETTING_STARTED.md)
- Check [ARCHITECTURE.md](../ARCHITECTURE.md) for system design

---

**Note:** Codespaces is free for 60 hours/month on the free tier. The environment will automatically stop after 30 minutes of inactivity to conserve hours.
