# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set a working directory in the container
WORKDIR /app

ARG AWS_REGION
ARG S3_BUCKET_NAME
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

# Convert ARGs into ENV variables
ENV AWS_REGION=$AWS_REGION \
    S3_BUCKET_NAME=$S3_BUCKET_NAME \
    AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
    
# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .
# Run database migrations and then start the application
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
