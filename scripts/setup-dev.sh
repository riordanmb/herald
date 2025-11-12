#!/bin/bash

# Herald Development Environment Setup Script
# This script sets up the complete development environment for Herald

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

# Main setup
print_header "Herald Development Environment Setup"

# Check prerequisites
print_header "Checking Prerequisites"

MISSING_DEPS=0

if ! check_command docker; then
    MISSING_DEPS=1
fi

if ! check_command docker-compose; then
    # Check if docker compose (v2) is available
    if docker compose version &> /dev/null; then
        print_success "docker compose (v2) is installed"
    else
        print_error "docker-compose is not installed"
        MISSING_DEPS=1
    fi
fi

if ! check_command node; then
    MISSING_DEPS=1
else
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ $NODE_VERSION -lt 18 ]; then
        print_warning "Node.js version is $NODE_VERSION, recommend 18 or higher"
    fi
fi

if ! check_command python3; then
    MISSING_DEPS=1
else
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [ "$(echo $PYTHON_VERSION | cut -d'.' -f1)" -lt 3 ] || [ "$(echo $PYTHON_VERSION | cut -d'.' -f2)" -lt 11 ]; then
        print_warning "Python version is $PYTHON_VERSION, recommend 3.11 or higher"
    fi
fi

if [ $MISSING_DEPS -eq 1 ]; then
    print_error "Missing required dependencies. Please install them and try again."
    exit 1
fi

# Create directory structure
print_header "Creating Directory Structure"

mkdir -p frontend/src/{app,components,lib,hooks,types,stores}
mkdir -p backend/{config,apps,static,media,logs}
mkdir -p backend/apps/{manuscripts,heraldry,recession,transcription,markup,search}
mkdir -p paleography/{app,tests}
mkdir -p infrastructure/docker/{nginx,postgres}
mkdir -p scripts
mkdir -p docs/{api,user-guide,development}

print_success "Directory structure created"

# Create environment files
print_header "Creating Environment Files"

# Backend .env
if [ ! -f backend/.env ]; then
    cat > backend/.env << 'EOF'
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://herald:herald_dev_password@localhost:5432/herald

# Redis
REDIS_URL=redis://localhost:6379/0

# MinIO/S3
STORAGE_BACKEND=minio
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=herald
MINIO_USE_SSL=False

# Paleography Service
PALEOGRAPHY_API_URL=http://localhost:8080

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1
EOF
    print_success "Created backend/.env"
else
    print_warning "backend/.env already exists, skipping"
fi

# Frontend .env.local
if [ ! -f frontend/.env.local ]; then
    cat > frontend/.env.local << 'EOF'
# API URLs
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_PALEOGRAPHY_API_URL=http://localhost:8080

# Authentication
NEXT_PUBLIC_AUTH_ENABLED=true

# Feature Flags
NEXT_PUBLIC_ENABLE_PALEOGRAPHY=true
NEXT_PUBLIC_ENABLE_RECESSION=true
EOF
    print_success "Created frontend/.env.local"
else
    print_warning "frontend/.env.local already exists, skipping"
fi

# Paleography .env
if [ ! -f paleography/.env ]; then
    cat > paleography/.env << 'EOF'
# Database
DATABASE_URL=postgresql://herald:herald_dev_password@localhost:5432/herald

# Redis
REDIS_URL=redis://localhost:6379/2

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=scribe-sim
MINIO_USE_SSL=False

# PyTorch
TORCH_DEVICE=cpu  # or cuda if GPU available

# Model
VISION_MODEL=facebook/dinov2-base
EOF
    print_success "Created paleography/.env"
else
    print_warning "paleography/.env already exists, skipping"
fi

# Docker Compose .env
if [ ! -f infrastructure/docker/.env ]; then
    cat > infrastructure/docker/.env << 'EOF'
# PostgreSQL
POSTGRES_DB=herald
POSTGRES_USER=herald
POSTGRES_PASSWORD=herald_dev_password

# Redis
REDIS_PASSWORD=

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin

# Ports
FRONTEND_PORT=3000
BACKEND_PORT=8000
PALEOGRAPHY_PORT=8080
POSTGRES_PORT=5432
REDIS_PORT=6379
MINIO_PORT=9000
MINIO_CONSOLE_PORT=9001
EOF
    print_success "Created infrastructure/docker/.env"
else
    print_warning "infrastructure/docker/.env already exists, skipping"
fi

# Create basic Docker Compose file
print_header "Creating Docker Compose Configuration"

if [ ! -f infrastructure/docker/docker-compose.yml ]; then
    cat > infrastructure/docker/docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: herald-postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: herald-redis
    ports:
      - "${REDIS_PORT}:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  minio:
    image: minio/minio:latest
    container_name: herald-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    ports:
      - "${MINIO_PORT}:9000"
      - "${MINIO_CONSOLE_PORT}:9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

volumes:
  postgres_data:
  redis_data:
  minio_data:

networks:
  default:
    name: herald-network
EOF
    print_success "Created infrastructure/docker/docker-compose.yml"
else
    print_warning "infrastructure/docker/docker-compose.yml already exists, skipping"
fi

# Git setup
print_header "Git Configuration"

if [ ! -f .gitattributes ]; then
    cat > .gitattributes << 'EOF'
# Auto detect text files and perform LF normalization
* text=auto

# Python
*.py text eol=lf
*.pyi text eol=lf
*.pyx text eol=lf
*.pyz text eol=lf

# JavaScript/TypeScript
*.js text eol=lf
*.jsx text eol=lf
*.ts text eol=lf
*.tsx text eol=lf
*.json text eol=lf

# Shell scripts
*.sh text eol=lf

# SQL
*.sql text eol=lf

# Docker
Dockerfile text eol=lf
*.dockerfile text eol=lf
docker-compose*.yml text eol=lf

# Binary files
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
*.woff binary
*.woff2 binary
*.ttf binary
*.eot binary
EOF
    print_success "Created .gitattributes"
fi

# Create placeholder files
print_header "Creating Placeholder Files"

# Backend requirements
mkdir -p backend/requirements
if [ ! -f backend/requirements/base.txt ]; then
    cat > backend/requirements/base.txt << 'EOF'
Django>=5.0,<5.1
djangorestframework>=3.14,<4.0
psycopg[binary]>=3.1,<4.0
django-environ>=0.11,<1.0
django-cors-headers>=4.3,<5.0
django-filter>=23.5,<24.0
Pillow>=10.1,<11.0
celery>=5.3,<6.0
redis>=5.0,<6.0
boto3>=1.34,<2.0
django-storages>=1.14,<2.0
drf-spectacular>=0.27,<1.0
EOF
    print_success "Created backend/requirements/base.txt"
fi

if [ ! -f backend/requirements/development.txt ]; then
    cat > backend/requirements/development.txt << 'EOF'
-r base.txt

# Development tools
black>=23.12,<24.0
isort>=5.13,<6.0
flake8>=7.0,<8.0
mypy>=1.8,<2.0
django-debug-toolbar>=4.2,<5.0
django-extensions>=3.2,<4.0
ipython>=8.20,<9.0

# Testing
pytest>=7.4,<8.0
pytest-django>=4.7,<5.0
pytest-cov>=4.1,<5.0
factory-boy>=3.3,<4.0
faker>=22.0,<23.0
EOF
    print_success "Created backend/requirements/development.txt"
fi

# Frontend package.json
if [ ! -f frontend/package.json ]; then
    cat > frontend/package.json << 'EOF'
{
  "name": "herald-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
    "test": "vitest",
    "test:coverage": "vitest --coverage"
  },
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tanstack/react-query": "^5.17.0",
    "zustand": "^4.4.7",
    "tailwindcss": "^3.4.0",
    "react-hook-form": "^7.49.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.3.0",
    "eslint": "^8.56.0",
    "eslint-config-next": "^14.1.0",
    "prettier": "^3.1.0",
    "vitest": "^1.1.0",
    "@testing-library/react": "^14.1.0",
    "@testing-library/jest-dom": "^6.1.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
EOF
    print_success "Created frontend/package.json"
fi

# Paleography requirements
if [ ! -f paleography/requirements.txt ]; then
    # Use the exact requirements from the specification
    cat > paleography/requirements.txt << 'EOF'
fastapi==0.115.5
uvicorn[standard]==0.32.0
python-multipart==0.0.12
pydantic==2.9.2
Pillow==11.0.0
opencv-python-headless==4.10.0.84
numpy==2.1.2
scikit-learn==1.5.2
umap-learn==0.5.6
transformers==4.45.2
torch==2.4.1
torchvision==0.19.1
redis==5.1.1
psycopg[binary]==3.2.3
minio==7.2.9
EOF
    print_success "Created paleography/requirements.txt"
fi

# Summary
print_header "Setup Complete!"

echo -e "Next steps:"
echo -e "  1. Review and update environment files in:"
echo -e "     - ${YELLOW}backend/.env${NC}"
echo -e "     - ${YELLOW}frontend/.env.local${NC}"
echo -e "     - ${YELLOW}paleography/.env${NC}"
echo -e ""
echo -e "  2. Start infrastructure services:"
echo -e "     ${YELLOW}cd infrastructure/docker${NC}"
echo -e "     ${YELLOW}docker-compose up -d${NC}"
echo -e ""
echo -e "  3. Set up backend:"
echo -e "     ${YELLOW}cd backend${NC}"
echo -e "     ${YELLOW}python -m venv venv${NC}"
echo -e "     ${YELLOW}source venv/bin/activate${NC}"
echo -e "     ${YELLOW}pip install -r requirements/development.txt${NC}"
echo -e ""
echo -e "  4. Set up frontend:"
echo -e "     ${YELLOW}cd frontend${NC}"
echo -e "     ${YELLOW}npm install${NC}"
echo -e ""
echo -e "  5. Set up paleography service:"
echo -e "     ${YELLOW}cd paleography${NC}"
echo -e "     ${YELLOW}python -m venv venv${NC}"
echo -e "     ${YELLOW}source venv/bin/activate${NC}"
echo -e "     ${YELLOW}pip install -r requirements.txt${NC}"
echo -e ""
echo -e "For detailed instructions, see ${GREEN}GETTING_STARTED.md${NC}"
echo -e ""

print_success "Herald development environment setup complete!"
