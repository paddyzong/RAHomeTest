# Introduction

Welcome to the **Data Type Inference and Conversion Web Application** project. This application is designed to process and display datasets with a focus on accurately inferring and converting data types using Python and Pandas. By handling data type inconsistencies and optimizing performance for large datasets, this tool aims to streamline data cleaning and preparation tasks.

Key features of the project include:

- **Advanced Data Type Inference:** Accurately identifies the most appropriate data type for each column in CSV or Excel files, addressing common issues where columns default to the 'object' data type.
- **Performance Optimization with Multithreading and Celery:** Efficiently processes large datasets by leveraging multithreading and Celery workers to avoid memory issues and reduce processing time.
- **Scalability with Kubernetes (EKS):** Deployed using Kubernetes (EKS on AWS and Minikube on local machine) to manage containerized applications, ensuring scalability and high availability.
- **Infrastructure as Code with Terraform and Terraform Cloud:** Utilizes Terraform for defining and provisioning infrastructure, while Terraform Cloud facilitates state management and automation.
- **Content Delivery with CloudFront and S3:** Implements Amazon S3 for static asset storage and Amazon CloudFront for global content delivery, enhancing performance and reliability.
- **Continuous Integration and Deployment with GitHub Actions:** Automates the building, testing, and deployment processes. GitHub Actions workflows build the frontend and push it to S3, build the backend and push it to Amazon Elastic Container Registry (ECR), and perform static code analysis using **Pylint** to ensure code quality and adherence to best practices.

- **Large File Uploads with TUS Protocol:** Supports resumable and reliable large file uploads using the TUS protocol, allowing users to upload big datasets seamlessly.
- **User-Friendly Interface:** Provides an intuitive interface that allows users to upload datasets, view processed data, and interact with the application effortlessly.

# Project Setup Guide

This guide provides instructions on how to set up and run the project. You have two options:

- **Option 1:** Run the project using Docker.
- **Option 2:** Set up and run the backend and frontend manually on your local machine.

---

## Prerequisites

Before you begin, ensure you have the following software installed:

- [Docker](https://www.docker.com/) (for Option 1)
- [Python](https://www.python.org/downloads/) 3.x (for Option 2)
- [Node.js and npm](https://nodejs.org/en/download/) (for Option 2)
- [Redis](https://redis.io/download) (for Option 2)
---

## Option 1: Running the Project with Docker

If you prefer to use Docker, follow these steps to build and run the Docker containers.

### Step 1: Build the Docker Containers

In the root directory of the project, run:

```bash
docker-compose build
```

### Step 2: Run the Docker Containers

Start the containers with:

```bash
docker-compose up
```

---

## Option 2: Running the Project Locally

Follow these steps to set up and run the backend and frontend on your local machine.

### Backend Setup

#### Step 1: Navigate to the Backend Directory

If your backend code is in a subdirectory, navigate to it:

```bash
cd Backend/RATypeInfer
```

#### Step 2: Create a Virtual Environment

Create a virtual environment named `venv`:

```bash
python -m venv venv
```

#### Step 3: Activate the Virtual Environment

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **On macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

#### Step 4: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt --break-system-packages
```
#### Step 5: Apply Database Migrations

Run the following commands to apply database migrations:

```bash
python manage.py migrate
```
#### Step 6: Configure Redis settings

Configure the redis settings in settings.py


#### Step 7: Run the Backend Application

Start the backend server:

```bash
python manage.py runserver
```

#### Step 8: Run Clery workers

Start a celery worker:

```bash
celery -A RATypeInfer worker --loglevel=info
```
### Frontend Setup

#### Step 1: Navigate to the Frontend Directory

If your frontend code is in a subdirectory, navigate to it:

```bash
cd Frontend/data-inference-app
```

#### Step 2: Install Dependencies

Install the required Node.js packages:

```bash
npm install
```

#### Step 3: Start the Frontend Application

Run the frontend application:

```bash
npm start
```

---

## Additional Information

### When Running Locally:

Backend server runs on http://localhost:8000/
Frontend application runs on http://localhost:3000/

### When Running with Docker:

Backend server runs on http://localhost:8000/
Frontend application runs on http://localhost/ (port 80)

---
