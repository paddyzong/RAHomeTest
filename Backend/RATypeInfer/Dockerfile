# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set a working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run database migrations and then start the application
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
