# Emergency Resource Management System
Georgia Tech OMSCS Database Concepts project.  Web application for managing
emergency resources built with Python, Flask, and MySQL.  Design requirements
for the project are in the specifications.pdf file.

## Quick Start

Get the application running locally with Docker and modern Python tooling.

### Prerequisites
- Docker & Docker Compose
- uv (Python package manager)

### Development Setup
```bash
# Install dependencies
uv sync

# Start services
docker compose up -d

# Access application
open http://localhost:5000
```

### Database Access
```bash
# Connect to MySQL
docker exec -it rms-mysql mysql -u root -p
# Password: password
```

## Development

Tools and commands for maintaining code quality and running tests.

### Code Quality
```bash
# Lint and format
ruff check .
ruff format .

# Run tests
pytest
```

## Test Users

Pre-configured user accounts for testing the application functionality.

- **user1** / password
- **user2** / password
- **user3** / password
- **user4** / password
