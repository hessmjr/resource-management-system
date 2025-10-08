# Resource Management System - Modernization Plan

## Current State
- Python 2.7 + Flask 0.11.1 (EOL/vulnerable)
- Ubuntu 14.04 Docker base (EOL)
- SQL injection vulnerabilities
- No modern tooling or testing

## Modernization Goals
Local development example project with modern best practices, not production deployment.

## Phase 1: Local Development Environment (Week 1)

### 1.1 Docker Compose Modernization
- Update to Docker Compose v3.8+
- Modern base images (Python 3.12 + Alpine/Ubuntu 22.04)
- Proper volume mounts and networking
- Development-optimized configuration

### 1.2 Python Tooling with uv + ruff
- Replace pip with uv for fast dependency management
- Add ruff for linting, formatting, and import sorting
- Configure pre-commit hooks
- Add pyproject.toml for modern Python packaging

## Phase 2: Backend Upgrade (Week 2)

### 2.1 Python + Flask Upgrade
- Python 2.7 → 3.12
- Flask 0.11.1 → 2.3+
- Update all dependencies to latest versions

### 2.2 Code Quality
- Fix SQL injection with parameterized queries
- Add password hashing (bcrypt)
- Implement proper error handling
- Add type hints and docstrings

### 2.3 Project Structure
- Restructure with Flask Blueprints
- Add SQLAlchemy ORM
- Implement proper configuration management

## Phase 3: Testing & Documentation (Week 3)

### 3.1 Testing Setup
- pytest with fixtures
- Database testing with SQLite
- Basic integration tests
- Coverage reporting

### 3.2 Development Workflow
- Local development scripts
- Database seeding/reset commands
- Automated formatting and linting

## Implementation Checklist

### Phase 1: Development Environment
- [ ] Modern Docker Compose setup
- [ ] Python 3.12 + Alpine base image
- [ ] uv package manager integration
- [ ] ruff configuration (linting + formatting)
- [ ] pyproject.toml setup

### Phase 2: Backend Modernization
- [ ] Python 2→3 migration
- [ ] Flask upgrade to 2.3+
- [ ] SQLAlchemy ORM implementation
- [ ] SQL injection fixes
- [ ] Password hashing (bcrypt)
- [ ] Flask Blueprints structure

### Phase 3: Quality & Testing
- [ ] pytest test suite
- [ ] Basic test coverage
- [ ] Pre-commit hooks
- [ ] Development scripts
- [ ] Documentation updates

## Quick Start Commands
```bash
# Development setup
uv sync
docker compose up -d

# Code quality
ruff check .
ruff format .

# Testing
pytest
```