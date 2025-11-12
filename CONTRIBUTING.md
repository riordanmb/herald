# Contributing to Herald

Thank you for your interest in contributing to Herald! This document provides guidelines and best practices for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Process](#development-process)
4. [Coding Standards](#coding-standards)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Testing Guidelines](#testing-guidelines)
8. [Documentation](#documentation)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- Read the [README.md](./README.md)
- Set up your development environment following [GETTING_STARTED.md](./GETTING_STARTED.md)
- Reviewed the [ARCHITECTURE.md](./ARCHITECTURE.md) to understand system design

### Finding Issues to Work On

1. **Good First Issues**: Look for issues labeled `good-first-issue`
2. **Help Wanted**: Check issues labeled `help-wanted`
3. **Feature Requests**: Review and discuss feature proposals
4. **Bug Reports**: Help fix reported bugs

### Claiming an Issue

Before starting work:
1. Comment on the issue to express interest
2. Wait for maintainer assignment/approval
3. Ask questions if requirements are unclear

## Development Process

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/herald.git
cd herald

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/herald.git
```

### 2. Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 3. Make Changes

- Write clean, readable code
- Follow coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

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

# Run all tests
./scripts/test-all.sh
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add manuscript comparison feature"
```

See [Commit Guidelines](#commit-guidelines) below.

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Coding Standards

### Python (Backend & Paleography)

**Style Guide:** PEP 8

**Formatting:**
```bash
# Use Black for code formatting
black .

# Use isort for import sorting
isort .

# Check with flake8
flake8 .
```

**Type Hints:**
```python
def get_manuscript(manuscript_id: UUID) -> Manuscript:
    """
    Retrieve a manuscript by ID.

    Args:
        manuscript_id: UUID of the manuscript

    Returns:
        Manuscript instance

    Raises:
        Manuscript.DoesNotExist: If manuscript not found
    """
    return Manuscript.objects.get(id=manuscript_id)
```

**Docstrings:**
Use Google-style docstrings:
```python
def complex_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Dictionary containing results

    Raises:
        ValueError: If param2 is negative
    """
    pass
```

### TypeScript (Frontend)

**Style Guide:** ESLint + Prettier configuration

**Formatting:**
```bash
# Format with Prettier
npm run format

# Lint with ESLint
npm run lint

# Auto-fix linting issues
npm run lint -- --fix
```

**Type Safety:**
```typescript
// Always define interfaces for data structures
interface Manuscript {
  id: string;
  shelfmark: string;
  repository: string;
  dateEarliest?: number;
  dateLatest?: number;
}

// Use strict types for functions
function getManuscript(id: string): Promise<Manuscript> {
  return fetch(`/api/v1/manuscripts/${id}`)
    .then(res => res.json());
}
```

**React Components:**
```typescript
// Use functional components with TypeScript
interface ManuscriptViewerProps {
  manuscriptId: string;
  onClose: () => void;
}

export default function ManuscriptViewer({
  manuscriptId,
  onClose
}: ManuscriptViewerProps) {
  // Component implementation
}
```

### SQL

**Naming Conventions:**
- Tables: lowercase, plural (e.g., `manuscripts`, `arms`)
- Columns: lowercase, snake_case (e.g., `created_at`, `bearer_name`)
- Indexes: `idx_{table}_{columns}` (e.g., `idx_manuscripts_shelfmark`)
- Foreign keys: `fk_{table}_{referenced_table}` (e.g., `fk_arms_manuscripts`)

### File Naming

**Python:**
- Modules: `lowercase_with_underscores.py`
- Classes: `CamelCase`
- Functions/variables: `lowercase_with_underscores`

**TypeScript:**
- Components: `PascalCase.tsx` (e.g., `ManuscriptViewer.tsx`)
- Utilities: `camelCase.ts` (e.g., `apiClient.ts`)
- Types: `types.ts` or `ComponentName.types.ts`

## Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) for clear commit history.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependencies

### Scopes

- `manuscripts`: Manuscript management
- `heraldry`: Heraldic features
- `paleography`: Paleography service
- `transcription`: Transcription features
- `search`: Search functionality
- `ui`: User interface
- `api`: API changes
- `db`: Database changes

### Examples

```bash
# Feature
git commit -m "feat(manuscripts): add surrogate upload functionality"

# Bug fix
git commit -m "fix(heraldry): correct tincture validation logic"

# Documentation
git commit -m "docs(api): update endpoint documentation"

# Breaking change
git commit -m "feat(api)!: change manuscript API response structure

BREAKING CHANGE: Manuscript API now returns ISO dates instead of timestamps"
```

### Commit Best Practices

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- First line is 50 characters or less
- Body wraps at 72 characters
- Separate subject from body with blank line
- Explain what and why, not how

## Pull Request Process

### Before Submitting

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commits follow conventional commits
- [ ] Branch is up to date with main

### PR Title

Use the same format as commit messages:
```
feat(manuscripts): add surrogate upload functionality
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Related Issue
Closes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**: CI must pass
2. **Code Review**: At least one approving review required
3. **Address Feedback**: Make requested changes
4. **Squash & Merge**: Maintainers will merge when ready

### After Merge

- Delete your feature branch
- Pull latest main
- Thank reviewers!

## Testing Guidelines

### Test Coverage

Aim for >80% test coverage:
- Unit tests for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows

### Writing Tests

**Backend (pytest):**
```python
# tests/test_manuscripts.py
import pytest
from apps.manuscripts.models import Manuscript


@pytest.mark.django_db
def test_create_manuscript():
    """Test manuscript creation with valid data."""
    manuscript = Manuscript.objects.create(
        shelfmark="MS Bodley 123",
        repository="Bodleian Library",
        material="parchment",
        folios=200
    )
    assert manuscript.shelfmark == "MS Bodley 123"
    assert manuscript.folios == 200


@pytest.mark.django_db
def test_manuscript_str_representation():
    """Test manuscript string representation."""
    manuscript = Manuscript.objects.create(
        shelfmark="MS Bodley 123",
        repository="Bodleian Library"
    )
    assert str(manuscript) == "MS Bodley 123"
```

**Frontend (Vitest + Testing Library):**
```typescript
// components/ManuscriptViewer.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ManuscriptViewer from './ManuscriptViewer';

describe('ManuscriptViewer', () => {
  it('renders manuscript shelfmark', () => {
    render(
      <ManuscriptViewer
        manuscript={{
          id: '123',
          shelfmark: 'MS Bodley 123',
          repository: 'Bodleian Library'
        }}
      />
    );

    expect(screen.getByText('MS Bodley 123')).toBeInTheDocument();
  });

  it('displays loading state', () => {
    render(<ManuscriptViewer isLoading={true} />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
});
```

### Test Organization

```
backend/
├── apps/
│   └── manuscripts/
│       └── tests/
│           ├── __init__.py
│           ├── test_models.py
│           ├── test_views.py
│           ├── test_serializers.py
│           └── factories.py

frontend/
└── src/
    └── components/
        └── ManuscriptViewer/
            ├── ManuscriptViewer.tsx
            ├── ManuscriptViewer.test.tsx
            └── index.ts
```

## Documentation

### Code Documentation

**Python:**
- Docstrings for all public modules, classes, and functions
- Type hints for all function parameters and returns
- Comments for complex logic

**TypeScript:**
- JSDoc for public functions and components
- Interface definitions for all data structures
- Comments for non-obvious code

### API Documentation

- Update OpenAPI schemas for endpoint changes
- Include request/response examples
- Document error responses
- Update Postman collection if available

### User Documentation

- Update user guide for new features
- Add screenshots for UI changes
- Write how-to guides for complex workflows
- Update FAQ if needed

### README Updates

Update README.md when:
- Adding new features
- Changing setup process
- Updating dependencies
- Adding new scripts

## Questions?

- Open a GitHub Discussion for general questions
- Comment on relevant issues for specific questions
- Contact maintainers via [contact method]

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Herald! 🎉
