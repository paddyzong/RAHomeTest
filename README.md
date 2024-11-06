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

#### Step 5: Run the Backend Application

Start the backend server:

```bash
python manage.py runserver
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
