# Getting Started with Herald Development

This guide will help you set up your development environment and start contributing to Herald.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Running the Application](#running-the-application)
4. [Development Workflow](#development-workflow)
5. [Common Tasks](#common-tasks)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **Git** (2.x+)
- **Docker** (20.x+) and **Docker Compose** (2.x+)
- **Node.js** (18.x or 20.x) and **npm** (9.x+)
- **Python** (3.11 or 3.12)

### Optional but Recommended
- **VS Code** or **PyCharm** (with appropriate extensions)
- **Postman** or **Insomnia** (for API testing)
- **TablePlus** or **pgAdmin** (for database management)

### System Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Disk Space**: 10GB for Docker images and dependencies
- **OS**: Linux, macOS, or Windows with WSL2

## Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd herald
```

### 2. Environment Configuration

Create environment files from templates:

```bash
# Backend environment
cp backend/.env.example backend/.env

# Frontend environment
cp frontend/.env.example frontend/.env.local

# Paleography service environment
cp paleography/.env.example paleography/.env

# Docker Compose environment
cp infrastructure/docker/.env.example infrastructure/docker/.env
```

Edit these files to configure:
- Database credentials
- Secret keys
- Storage settings
- API endpoints

### 3. Quick Setup with Docker Compose

The easiest way to get started:

```bash
# Navigate to docker directory
cd infrastructure/docker

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- MinIO (port 9000, console on 9001)
- Django API (port 8000)
- FastAPI Paleography (port 8080)
- Next.js Frontend (port 3000)

### 4. Initialize the Database

```bash
# Run Django migrations
docker-compose exec backend python manage.py migrate

# Create a superuser
docker-compose exec backend python manage.py createsuperuser

# Load initial data (heraldic tinctures, charges)
docker-compose exec backend python manage.py loaddata initial_heraldry
```

### 5. Verify Installation

Visit these URLs to verify everything is working:

- **Frontend**: http://localhost:3000
- **Django Admin**: http://localhost:8000/admin
- **Django API**: http://localhost:8000/api/v1/
- **Paleography API Docs**: http://localhost:8080/docs
- **MinIO Console**: http://localhost:9001 (default: minioadmin/minioadmin)

## Running the Application

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# Start specific service
docker-compose up frontend

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs -f [service_name]
```

### Running Services Individually

#### Backend (Django)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

# In another terminal, start Celery worker (for async tasks)
celery -A config worker -l INFO
```

#### Frontend (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

#### Paleography Service (FastAPI)

```bash
cd paleography

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

#### Database (PostgreSQL)

```bash
# Using Docker
docker run -d \
  --name herald-postgres \
  -e POSTGRES_DB=herald \
  -e POSTGRES_USER=herald \
  -e POSTGRES_PASSWORD=herald_dev_password \
  -p 5432:5432 \
  postgres:16-alpine

# Or install PostgreSQL locally and create database
createdb herald
```

#### Cache (Redis)

```bash
# Using Docker
docker run -d \
  --name herald-redis \
  -p 6379:6379 \
  redis:7-alpine
```

#### Object Storage (MinIO)

```bash
# Using Docker
docker run -d \
  --name herald-minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio server /data --console-address ":9001"
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit files in your preferred IDE. The development servers have hot reload enabled:
- Frontend: Changes in `frontend/src/` auto-reload
- Backend: Django auto-reloads on Python file changes
- Paleography: FastAPI auto-reloads with `--reload` flag

### 3. Run Tests

```bash
# Backend tests
cd backend
pytest

# Run specific test
pytest apps/manuscripts/tests/test_models.py

# With coverage
pytest --cov=apps --cov-report=html

# Frontend tests
cd frontend
npm test

# Run specific test
npm test -- ManuscriptViewer.test.tsx

# With coverage
npm test -- --coverage

# Paleography tests
cd paleography
pytest
```

### 4. Format Code

```bash
# Backend - Black + isort
cd backend
black .
isort .

# Frontend - Prettier + ESLint
cd frontend
npm run format
npm run lint

# Or use auto-format in VS Code (recommended)
```

### 5. Commit Changes

Use conventional commit messages:

```bash
git add .
git commit -m "feat(manuscripts): add surrogate upload functionality"

# Commit types: feat, fix, docs, style, refactor, test, chore
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Common Tasks

### Add a New Django Model

1. Create model in appropriate app:
   ```python
   # backend/apps/yourapp/models.py
   class YourModel(models.Model):
       # fields...
   ```

2. Create migration:
   ```bash
   python manage.py makemigrations
   ```

3. Apply migration:
   ```bash
   python manage.py migrate
   ```

4. Add serializer:
   ```python
   # backend/apps/yourapp/serializers.py
   class YourModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = YourModel
           fields = '__all__'
   ```

5. Create viewset and register URL

### Add a New API Endpoint

1. Create viewset in `views.py`
2. Add serializer in `serializers.py`
3. Register route in `urls.py`
4. Write tests in `tests/`
5. Update API documentation

### Add a New React Component

1. Create component file:
   ```typescript
   // frontend/src/components/yourcomponent/YourComponent.tsx
   export default function YourComponent() {
     return <div>Your component</div>
   }
   ```

2. Add tests:
   ```typescript
   // frontend/src/components/yourcomponent/YourComponent.test.tsx
   import { render, screen } from '@testing-library/react'
   import YourComponent from './YourComponent'

   describe('YourComponent', () => {
     it('renders correctly', () => {
       render(<YourComponent />)
       expect(screen.getByText('Your component')).toBeInTheDocument()
     })
   })
   ```

3. Export from index:
   ```typescript
   // frontend/src/components/yourcomponent/index.ts
   export { default } from './YourComponent'
   ```

### Seed Test Data

```bash
# Backend - create fixture
python manage.py dumpdata manuscripts.Manuscript --indent 2 > fixtures/manuscripts.json

# Load fixture
python manage.py loaddata manuscripts

# Or create custom management command
python manage.py seed_manuscripts --count 100
```

### Access Database

```bash
# Using Django shell
python manage.py shell_plus

# Using psql
docker-compose exec postgres psql -U herald

# Using TablePlus or pgAdmin
# Host: localhost
# Port: 5432
# Database: herald
# User: herald
# Password: (from .env file)
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Django logs
tail -f backend/logs/django.log

# Frontend logs (in browser console)
# Or terminal where npm run dev is running
```

### Reset Database

```bash
# Drop and recreate database
docker-compose down -v
docker-compose up -d postgres
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :3000  # or :8000, :8080

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml or .env
```

### Docker Issues

```bash
# Clean up Docker
docker-compose down
docker system prune -a

# Rebuild images
docker-compose build --no-cache

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Database Connection Issues

1. Check PostgreSQL is running:
   ```bash
   docker-compose ps postgres
   ```

2. Verify credentials in `.env`

3. Check database exists:
   ```bash
   docker-compose exec postgres psql -U herald -l
   ```

### Node Module Issues

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Next.js cache
rm -rf .next
```

### Python Dependency Issues

```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
```

### MinIO Access Issues

1. Check MinIO is running:
   ```bash
   docker-compose ps minio
   ```

2. Access console: http://localhost:9001

3. Create bucket named `herald` (or as configured)

4. Set bucket policy to public or configure access keys

### Hot Reload Not Working

**Frontend:**
- Check webpack config
- Ensure files are saved
- Check browser console for errors

**Backend:**
- Restart Django server
- Check for syntax errors
- Verify `DEBUG=True` in settings

## Next Steps

1. Read [ARCHITECTURE.md](./ARCHITECTURE.md) to understand system design
2. Review [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines
3. Check [docs/](./docs/) for detailed documentation
4. Join the development chat/forum (if available)
5. Pick an issue labeled "good first issue" to start contributing

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: [Contact email]
- **Chat**: [Discord/Slack link]

---

Happy coding! 🚀
