### Bookly — FastAPI Backend 
Bookly is a modern backend service built using FastAPI, designed to power a scalable book review and social interaction platform. It provides a robust RESTful API that enables users to explore books, share reviews, interact with authors, and engage through posts, likes, and comments.

This project focuses on clean architecture, asynchronous operations, and production-ready backend practices, making it ideal for learning and building real-world API systems.


## Getting Started
Follow the instructions below to set up and run your FastAPI project.

### Prerequisites
Ensure you have the following installed:

- Python >= 3.10
- PostgreSQL
- Redis

### Project Setup
1. Clone the project repository:
    ```bash
    git clone https://github.com/0xakd/fastapi_backend_assignment.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd fastapi_backend_assignment/
    ```

3. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run database migrations to initialize the database schema:
    ```bash
    alembic upgrade head
    ```

6. Open a new terminal and ensure your virtual environment is active. Start the Celery worker (Linux/Unix shell):
    ```bash
    sh runworker.sh
    ```

## Running the Application
Start the application:

```bash
fastapi dev src/
```
Alternatively, you can run the application using Docker:
```bash
docker compose up -d
```
## Running Tests
Run the tests using this command
```bash
pytest
```
