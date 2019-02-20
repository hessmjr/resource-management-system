# Emergency Resource Management System
Georgia Tech OMSCS Database Concepts project.  Web application for managing
emergency resources built with Python, Flask, and MySQL.  Design requirements
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

1. `docker/up.sh`  - this starts all the necessary components
2. `docker/bash.sh` - this logs into the web app and lets you run bash commands

After executing those commands you will be logged into the virtual machine and
in the project directory on the VM.  When finished you may exit the VM and
then execute to clean up:

1. `docker/down.sh`

### Start-Up
The service runs when Docker is initially started using `docker/up.sh`.  If you
need to access the process then the following can help:

1. Once everything is complete execute the command `docker/bash.sh` to log into
   the Virtual Machine
2. Navigate to the project by executing `cd code`
3. To re-start the flask server from the same directory execute
   `python src/main.py`
    - You can now reach the app from your computer's browser, just go to
    `http://localhost:5000/`

**Database**
MySQL also should be currently running now and is reachable from logging into
its Docker container as well, login with the following:
    - user: root
    - password: password
    - Ex: `mysql -h 127.0.0.1 -u root --password='password'` should open the
    MySQL prompt


## Usage
The application should be reachable from your browser at `http://localhost:5000/`
once the Vagrant box is running.  There are 4 users built into the application
for testing and all use the password `password`:

- user1
- user2
- user3
- user4
