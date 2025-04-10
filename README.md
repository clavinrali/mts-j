# EEN1037 mts-j

## Overview

A full-stack django based framework for a factory machinery status and repair tracking system. This project is a group assignment for EEN1037 module

## Developing

### Launching the Project in Visual Studio Code

1. Open the project directory in Visual Studio Code.
2. Navigate to the `Run and Debug` panel or press `F5`.
3. Select and execute the desired launch configuration, such as `python manage.py runserver`.

### Setting Up MySQL

To configure the project to use MySQL as the database backend:

1. Install MySQL on your system and create a new database for the project and create a superuser.
  ```
  mysql -u root -p
  ```
  ```mysql
  CREATE DATABASE my_database;
  CREATE USER 'my_username'@'localhost' IDENTIFIED BY 'my_password';
  GRANT ALL PRIVILEGES ON my_database.* TO 'my_username'@'localhost';
  FLUSH PRIVILEGES;
  ```
2. Install the MySQL client library for Python:
  ```
  pip install mysqlclient
  ```
3. create a the `.env` file with those information:
  ```python
  DB_ENGINE=django.db.backends.mysql
  DB_NAME=my_database # change this field
  DB_USER=my_username # change this field
  DB_PASSWORD=my_password # change this field
  DB_HOST=localhost # Use "localhost" if you are on a Linux machine but change with "host.docker.internal" if you are on Windows or Mac and using docker
  DB_PORT=3306
  DB_CHARSET=utf8mb4
  ```
4. Apply migrations to the MySQL database:
  ```
  python manage.py migrate
  ```
5. Run the development server to verify the setup:
  ```
  python manage.py runserver
  ```

### Creating New Database Schema Migrations

Whenever you modify any `Model` classes in the `models.py` files, you need to create corresponding SQL schema migration files. This process is automated using the `makemigrations` command:

* Steps to Generate Migrations:
  * Use the `Run and Debug` feature and execute the `Django makemigrations` command.

Ensure that the generated migration files are committed alongside your source code.


### Applying database migrations to the test database

* Run and Debug
  * `python manage.py makemigrations mts-j`
  * `python manage.py runserver`
  * `python manage.py migrate`

### Creating a Super User

if you want to create a super user to add some information with the Django interface:

1. Enter in this command to initialize the super user
  ```
  python manage.py createsuperuser
  ```
2. Specify your personal information
  ```
  Username (leave blank to use 'your-username'): admin
  Email address: admin@example.com
  Password:
  Password (again):
  Superuser created successfully.
  ```
3. Verify with this URL `http://127.0.0.1:8000/admin/`

## Running as a Docker container

A sample Dockerfile is provided which will build and run the application.

It mounts one Docker volume on /app/storage for local file storage, and will connect to an SQL database specified with the environment variable "DATABASE_URL".

If "DATABASE_URL" is blank, it will default to an SQLite database on the /app/storage volume.


### Building and running the Docker container

Install [Docker](https://www.docker.com/) on your system.

You can use Visual Studio Code "Docker" plugin, or the included build tasks (Ctrl+P + "task") or these command line commands:

To build:
```
docker build . -t mts-j
```

To create a persistent storage volume:
```
docker volume create mts-j-storage
```

To run the container:
```
docker run -ti -v mts-j-storage:/app/storage -p 8000:8000 mts-j
```

To delete the persistent volume (i.e. any stored files and test databases)
```
docker volume rm mts-j-storage
```
