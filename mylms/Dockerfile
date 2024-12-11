
FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY .. .
CMD python manage.py runserver 0.0.0.0:80
#CMD gunicorn mylms.wsgi:application --bind 0.0.0.0:8080


## Use Python 3.9 on Alpine Linux
#FROM python:3.9-alpine
#
## Set environment variable to prevent Python from buffering stdout/stderr
#ENV PYTHONUNBUFFERED 1
#
## Set working directory
#WORKDIR /app
#
## Copy requirements file
#COPY requirements.txt .
#
## Install system dependencies required for mysqlclient and other packages
#RUN apk update && \
#    apk add --no-cache \
#        mariadb-connector-c-dev \
#        gcc \
#        libc-dev \
#        musl-dev \
#        python3-dev \
#        libffi-dev \
#        pkgconfig && \
#    pip install --upgrade pip && \
#    pip install -r requirements.txt
#
## Copy the application code
#COPY . .
#
## Run the Django application
#CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

#FROM python:3.9-alpine
#ENV PYTHONUNBUFFERED 1
#
## Set the working directory in the container
#WORKDIR /app
#
## Copy the requirements file and install dependencies
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#
## Copy the rest of the application files
#COPY . .
#
## Use gunicorn to serve the application on port 8080
#CMD gunicorn mylms.wsgi:application --bind 0.0.0.0:8080
