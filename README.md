# Async Document Processing System

## Overview

This project is a backend system for processing documents asynchronously.
It is built using FastAPI for APIs, PostgreSQL for storage, Redis as a message broker, and Celery for background task execution.

The main idea is to allow users to upload documents and process them without blocking the main application.

---

## Setup

1. Clone the project and open it:

   ```bash
   git clone <repo-link>
   cd async-doc-processing
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a PostgreSQL database named `doc_processing` and update the database URL in the config file.

5. Make sure Redis is installed and available.

---

## Running the Project

Start the services in separate terminals:

* FastAPI server:

  ```bash
  uvicorn app.main:app --reload
  ```

* Redis:

  ```bash
  redis-server
  ```

* Celery worker:

  ```bash
  celery -A worker.celery_app worker --pool=solo --loglevel=info
  ```

---

## How It Works

1. A file is uploaded through the API.
2. The file is stored locally and a database record is created.
3. A processing request is sent to Celery.
4. The worker reads the file and performs basic processing.
5. The result is saved in the database.
6. The user can check the status anytime.

---

## Architecture

FastAPI handles incoming requests, Redis acts as a queue, and Celery processes tasks in the background. PostgreSQL stores all document-related data.

---


## Trade-offs

* Local storage was used instead of cloud storage to keep the setup simple.
* Processing logic is basic and meant for demonstration.
* Celery runs in solo mode due to Windows compatibility.

---



## Author

Darshita Singh
