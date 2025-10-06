# Emergency Resource Management System
Georgia Tech OMSCS Database Concepts project. Web application for managing
emergency resources built with Python, Flask, and MySQL. Design requirements
for the project are in the specifications.pdf file.

## Development
Instructions and dependencies needed for development

### Dependencies:
You'll need the following tools to run the application:

- [Docker]()
- [Docker Compose]()

To use Docker, ensure that you have [Docker](https://www.docker.com/) and
[Docker Compose](https://docs.docker.com/compose/) installed properly. Then,
from the project directory, issue the following commands:

1. `docker-compose up -d` - this starts all the necessary components (backend, frontend, and database)

After executing those commands you will have the application running. When finished you may clean up with:

1. `docker-compose down`

### Start-Up
The service runs when Docker is initially started using `docker-compose up -d`. If you
need to access the process then the following can help:

1. Once everything is complete the application will be available at `http://localhost:3000`
2. The backend API is available at `http://localhost:5000`
3. To re-start the flask server manually, execute `docker-compose exec backend python run.py`

**Database**
MySQL also should be currently running now and is reachable from logging into
its Docker container as well, login with the following:
    - user: root
    - password: password
    - Ex: `docker-compose exec mysql mysql -u root --password='password'` should open the
    MySQL prompt

## Usage
The application should be reachable from your browser at `http://localhost:3000/`
once the Docker containers are running. There are 4 users built into the application
for testing and all use the password `password`:

- user1
- user2
- user3
- user4