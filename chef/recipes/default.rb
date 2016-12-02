
# update linux environment
execute "apt-get update" do
    command "apt-get update"
end

# python runtime version and app requirements
python_runtime '2'
pip_requirements '/home/gatech/resource-management-system/requirements.txt'

# install python mysql connector used by dbConnect
apt_package "python-mysql.connector" do
	action :install
end

# install and setup MySQL
mysql_service 'mysql_db' do
    port '3306'
    version '5.6'
    initial_root_password 'password'
    action [:create, :start]
end

# create main database
execute "create main db" do
    command "mysql -h 127.0.0.1 -u root --password='password' -e 'CREATE DATABASE IF NOT EXISTS erms'"
end

# run creation script on database
execute 'run creation script' do
    command "mysql -h 127.0.0.1 -u root --password='password' erms" +
        " < /home/gatech/resource-management-system/src/sql/creation_script.sql"
end

# run creation script on database
execute 'run insertion script' do
    command "mysql -h 127.0.0.1 -u root --password='password' erms" +
        " < /home/gatech/resource-management-system/src/sql/insert_statements_script.sql"
end

# supervisor setup
include_recipe "supervisor"

cookbook_file "/etc/supervisord.conf" do
    source "supervisord.conf"
    mode 0644
end

# Start supervisor to handle start and restarting server
supervisor_service "bowling-tracker" do
    action :enable
    directory "/home/gatech/resource-management-system"
    command "python src/main.py"
    stdout_logfile "/home/gatech/resource-management-system/.log"
    stdout_logfile_maxbytes "50MB"
    redirect_stderr true
end
