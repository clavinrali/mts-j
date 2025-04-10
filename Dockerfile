# Use the official Python image as the base
FROM python:3.13

# Create a directory to store the application code and the database
RUN mkdir /app /app/storage

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . /app/

# Project specific configuration
ENV DJANGO_SUPERUSER_USERNAME "admin"
ENV DJANGO_SUPERUSER_PASSWORD "admin"
ENV DJANGO_SUPERUSER_EMAIL "admin@localhost"
ENV DATABASE_URL "/usr/sbin/mysqld/mysqld.sock"

# Expose port 8000 to access the Django application
EXPOSE 8000

# Command to run migrations and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
