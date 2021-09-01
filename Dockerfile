# Use an local Python with taipei time as a parent image
FROM solarservice/python:taipei_time

# Set the container working directory to /opt/SolarPlatForm_Backend
# if no such dir, create new one automatically
WORKDIR /Send_IP_for_me


# Copy the directory where Dockerfile at, into the container at /opt/SolarPlatForm_Backend
COPY  . /Send_IP_for_me

# Install any needed packages specified in requirements.txt
RUN python -m pip install --trusted-host pypi.python.org --upgrade pip
RUN python -m pip install --trusted-host pypi.python.org --upgrade setuptools
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update
RUN apt-get -y install iputils-ping
RUN apt-get -y install vim
RUN apt-get -y install procps
RUN apt-get -y install cron
