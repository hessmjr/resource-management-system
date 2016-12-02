# Emergency Resource Management System
Georgia Tech OMSCS Database Concepts project.  Web application for managing emergency resources built with Python, Flask, and MySQL.  Design requirements for the project are in the specifications.pdf file.

## Development
Instructions and dependencies needed for development

### Dependencies:
You'll need the following tools to run the application:

- [Virtual Box](https://www.virtualbox.org/)
- [ChefDK](https://downloads.chef.io/chef-dk/mac/)
- [Vagrant](https://www.vagrantup.com/downloads.html)
    - [Vagrant Berkshelf Plugin](https://github.com/berkshelf/vagrant-berkshelf)
    - [Vagrant Omnibus Plugin](https://github.com/chef/vagrant-omnibus)

### Start-Up
In order to use

1. From the project root directory execute the command `vagrant up` from your command line
2. Once everything is complete execute the command `vagrant ssh` to log into the Virtual Machine
3. Navigate to the project by executing `cd ../gatech/resource-management-system`
5. To start the flask server from the same directory execute `python src/main.py`
    - You can now reach the app from your computer's browser, just go to `http://localhost:5000/`
4. MySQL also should be currently running now and should be reachable from the shell within the VM, login with the following:
    - user: root
    - password: password
    - Ex: `mysql -h 127.0.0.1 -u root --password='password'` should open the MySQL prompt


## Usage
The application should be reachable from your browser at `http://localhost:5000/` once the Vagrant box is running.  There are 4 users built into the application for testing and all use the password `password`:

- user1
- user2
- user3
- user4


## TODO

- [x] clean up
- [x] fix UUID bug
- [x] consolidate custom JS
- [ ] fix date bug
- [ ] resources available NOW when not bug
- [x] totals at bottom of resource report
- [x] change name of schema to erms
- [x] ensure deploy and start
