# Herald

A comprehensive digital platform for heraldic manuscript research, enabling scholars to catalog, annotate, compare, and analyze medieval heraldic manuscripts.

## Overview

Herald provides:

- **Manuscript Management**: Catalog manuscripts with rich metadata and multiple surrogates
- **Heraldic Markup**: Annotate coats of arms according to heraldic rules
- **Arms Comparison**: Compare heraldic imagery across manuscripts
- **Recession Tracking**: Build and visualize manuscript family trees
- **Transcription**: Transcribe medieval texts with paleographic support
- **Heraldic Search**: Advanced search across blazons, charges, and tinctures
- **Paleography Analysis**: ML-powered scribal hand similarity detection

## Architecture

Herald is built as a modern web application with microservices:

- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Core API**: Django 5 with Django REST Framework
- **Paleography Service**: FastAPI with PyTorch/DINOv2
- **Database**: PostgreSQL 16
- **Object Storage**: MinIO (S3-compatible)
- **Cache**: Redis 7

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture documentation.

## Project Structure

```
herald/
├── frontend/          # Next.js frontend application
├── backend/           # Django REST API
├── paleography/       # FastAPI paleography microservice
├── infrastructure/    # Docker, K8s, and deployment configs
├── scripts/           # Utility scripts
└── docs/              # Documentation
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd herald
   ```

2. **Run the setup script**
   ```bash
   ./scripts/setup-dev.sh
   ```

3. **Start all services**
   ```bash
   cd infrastructure/docker
   docker-compose up
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Django API: http://localhost:8000
   - Paleography API: http://localhost:8080
   - MinIO Console: http://localhost:9001

### Manual Setup

If you prefer to set up services individually:

#### Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/development.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

#### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

#### Paleography Service (FastAPI)
```bash
cd paleography
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

## Development Workflow

### Creating a New Feature

1. Create a feature branch from `main`
2. Make your changes following the coding standards
3. Write tests for new functionality
4. Run the test suite
5. Submit a pull request

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Paleography tests
cd paleography
pytest
```

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **TypeScript**: Follow project ESLint/Prettier configs
- **Commits**: Use conventional commit messages

## Documentation

- [Architecture](./ARCHITECTURE.md) - System architecture and design
- [Development Roadmap](./ARCHITECTURE.md#development-roadmap) - Planned features and timeline
- [API Documentation](./docs/api/) - API endpoints and usage
- [User Guide](./docs/user-guide/) - End-user documentation

## Features by Phase

### Phase 1: Foundation ✅ (Target: Week 4)
- Infrastructure setup
- Basic manuscript CRUD
- Image upload and storage
- User authentication

### Phase 2: Viewing & Markup (Target: Week 8)
- High-resolution image viewer
- Annotation system
- Folio navigation

### Phase 3: Heraldry Core (Target: Week 12)
- Heraldic data models
- Shield markup tools
- Blazon editor

### Phase 4: Search & Comparison (Target: Week 16)
- Full-text search
- Arms comparison
- Similarity metrics

### Phase 5: Recession (Target: Week 20)
- Manuscript relationships
- Stemma visualization

### Phase 6: Transcription (Target: Week 23)
- Text transcription
- Special characters
- Search integration

### Phase 7: Paleography (Target: Week 28)
- Scribe similarity analysis
- Visual embeddings
- Clustering

### Phase 8: Polish (Target: Week 32)
- Performance optimization
- Comprehensive testing
- Documentation
- Production deployment

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Guidelines

1. **Code Quality**
   - Write tests for new features
   - Maintain >80% test coverage
   - Follow existing code patterns

2. **Documentation**
   - Update API docs for endpoint changes
   - Add JSDoc/docstrings for public functions
   - Update user guides for UI changes

3. **Accessibility**
   - Ensure WCAG AA compliance
   - Test with screen readers
   - Provide keyboard navigation

## Technology Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript 5
- React 18
- Tailwind CSS 3
- shadcn/ui components
- React Query (TanStack Query)
- OpenSeadragon (image viewer)
- Fabric.js (annotations)

### Backend
- Django 5
- Django REST Framework 3.14
- PostgreSQL 16
- Redis 7
- Celery (task queue)

### Paleography Service
- FastAPI 0.115
- PyTorch 2.4
- Transformers (Hugging Face)
- DINOv2 vision model
- scikit-learn
- OpenCV

### Infrastructure
- Docker & Docker Compose
- Nginx (reverse proxy)
- MinIO (object storage)
- PostgreSQL (database)
- Redis (cache)

## License

[License information to be added]

## Contact

[Contact information to be added]

## Acknowledgments

This project builds upon the rich tradition of heraldic scholarship and modern advances in computer vision and machine learning.

Special thanks to:
- The paleography service design provided in the initial specification
- The open-source community for the excellent tools and libraries
- Medieval manuscript repositories for inspiration

---

**Status**: In Planning Phase
**Version**: 0.1.0-alpha
**Last Updated**: 2025-11-12
