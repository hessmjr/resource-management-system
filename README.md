# Emergency Resource Management System (ERMS)

A modernized web application for managing emergency resources and incidents, built with Python Flask backend and a clean frontend interface.

## Project Structure

```
erms/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── auth.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── user_service.py
│   │       ├── resource_service.py
│   │       └── incident_service.py
│   ├── tests/
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── run.py
│   └── Dockerfile
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   ├── materialize.min.css
│   │   │   └── custom.css
│   │   ├── js/
│   │   │   ├── jquery-latest.min.js
│   │   │   ├── materialize.min.js
│   │   │   └── app.js
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── menu.html
│       ├── add_resource.html
│       ├── search_resources.html
│       ├── search_results.html
│       └── components/
│           └── navbar.html
├── src/
│   ├── sql/
│   │   ├── creation_script.sql
│   │   └── insert_statements_script.sql
│   └── (legacy files)
├── docker/
│   └── (existing docker files)
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Features

- **User Authentication**: Secure login system with session management
- **Resource Management**: Add, search, and manage emergency resources
- **Incident Management**: Create and track emergency incidents
- **Advanced Search**: Search resources by keyword, ESF, location, and incident
- **Modern UI**: Clean, responsive interface built with Materialize CSS
- **Service Layer Architecture**: Clean separation of concerns with service classes
- **Database Integration**: Direct SQL queries with MySQL database

## Technology Stack

### Backend
- **Python 3.11+**
- **Flask 2.3.3** - Web framework
- **MySQL 8.0** - Database
- **mysql-connector-python** - Database connector

### Frontend
- **HTML5** - Markup
- **Materialize CSS** - UI framework
- **JavaScript** - Client-side functionality
- **jQuery** - DOM manipulation

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server (frontend)

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd erms
   ```

2. **Set up database credentials**
   ```bash
   cp credentials.json.example credentials.json
   # Edit credentials.json with your database configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - MySQL: localhost:3306

### Development Setup

1. **Backend Development**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   # Serve static files with any HTTP server
   python -m http.server 3000
   ```

## API Endpoints

### Authentication
- `GET /` - Login page
- `POST /` - Login authentication
- `GET /logout` - Logout

### Main Application
- `GET /menu` - Main menu
- `GET /add-resource` - Add resource form
- `POST /add-resource` - Create new resource
- `GET /search-resources` - Search form
- `POST /search-resources` - Search resources

## Database Schema

The application uses a MySQL database with the following main tables:
- `user` - User accounts
- `resource` - Emergency resources
- `incident` - Emergency incidents
- `esf` - Emergency Support Functions
- `resource_request` - Resource requests
- `resource_repair` - Resource repair records

## Configuration

### Environment Variables
- `FLASK_ENV` - Flask environment (development/production)
- `DATABASE_CONFIG_FILE` - Path to database credentials file
- `SECRET_KEY` - Flask secret key for sessions

### Database Configuration
Create a `credentials.json` file with your database configuration:
```json
{
  "host": "localhost",
  "user": "root",
  "password": "password",
  "database": "erms"
}
```

## Testing

Run tests for the backend:
```bash
cd backend
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of a Georgia Tech OMSCS Database Concepts course project.

## Support

For issues and questions, please refer to the project documentation or contact the development team.