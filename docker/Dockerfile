# Use an official Python runtime as a parent image
FROM ubuntu:14.04
FROM python:2.7-slim

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port available to the world outside this container
EXPOSE 5000

RUN apt-get update
RUN apt-get install -y python-mysql.connector

# Run app.py when the container launches
CMD ["python", "src/main.py"]
