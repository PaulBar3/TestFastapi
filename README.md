# TestFastAPI Application

This is a FastAPI web application with user management, blog posts, and basic CRUD operations.

## Features

- User registration and authentication
- Blog post creation and management
- RESTful API endpoints
- Async database operations with SQLAlchemy
- Pydantic models for data validation

## Prerequisites

- Python 3.13+
- uv package manager

## Installation

1. Clone the repository
2. Install uv if you don't have it: `pip install uv`
3. Create a virtual environment: `uv venv .venv`
4. Activate the virtual environment: `source .venv/bin/activate`
5. Install dependencies: `uv pip install fastapi uvicorn pydantic sqlalchemy asyncpg python-multipart`
6. Run the application: `python run_server.py`

Alternatively, you can run the application directly using:
```bash
source .venv/bin/activate && python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)"
```

## Endpoints

- `GET /` - Home page
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get a specific user
- `POST /users/` - Create a new user
- `PUT /users/{user_id}` - Update a specific user
- `DELETE /users/{user_id}` - Delete a specific user
- `GET /posts/` - Get all blog posts
- `GET /posts/{post_id}` - Get a specific blog post
- `POST /posts/` - Create a new blog post
- `PUT /posts/{post_id}` - Update a specific blog post
- `DELETE /posts/{post_id}` - Delete a specific blog post

## API Documentation

Interactive API documentation is available at `http://localhost:8000/docs` after starting the server.