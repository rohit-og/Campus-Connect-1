# Campus Connect API Documentation

## Overview

The Campus Connect backend API is built with FastAPI and provides comprehensive endpoints for:
- User authentication (JWT-based)
- Resume parsing and management
- ATS (Applicant Tracking System) scoring
- Feedback generation for rejected candidates
- Student job search and skill gap analysis
- Job and candidate management

## Database Architecture

- **PostgreSQL**: Stores structured relational data (users, jobs, applications, candidates, evaluations)
- **MongoDB**: Stores unstructured/flexible data (resume raw text, detailed feedback, logs, job descriptions)

## API Endpoints

### Authentication (`/api/v1/auth`)

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user information
- `POST /api/v1/auth/refresh` - Refresh access token

### Resume Management (`/api/v1/resume`)

- `POST /api/v1/resume/parse` - Parse resume from text
- `POST /api/v1/resume/upload` - Upload and parse resume file (PDF/DOCX)
- `GET /api/v1/resume/{resume_id}` - Get parsed resume data

### ATS Scoring (`/api/v1/ats`)

- `POST /api/v1/ats/score` - Score resume against job requirements
- `GET /api/v1/ats/evaluation/{evaluation_id}` - Get evaluation details
- `POST /api/v1/ats/batch-score` - Score multiple resumes

### Feedback Generation (`/api/v1/feedback`)

- `POST /api/v1/feedback/generate` - Generate feedback for rejected candidate
- `GET /api/v1/feedback/{feedback_id}` - Get feedback details
- `GET /api/v1/feedback/candidate/{candidate_id}` - Get all feedback for a candidate

### Student Features (`/api/v1/student`)

- `POST /api/v1/student/jobs/search` - Natural language job search
- `POST /api/v1/student/skill-gap/analyze` - Analyze skill gap between student and job
- `POST /api/v1/student/resume/feedback` - Get resume feedback for ATS optimization
- `POST /api/v1/student/rejection/interpret` - Interpret rejection feedback

### Job Management (`/api/v1/jobs`)

- `GET /api/v1/jobs` - List all jobs (with pagination and filters)
- `POST /api/v1/jobs` - Create new job posting (recruiters/admins only)
- `GET /api/v1/jobs/{job_id}` - Get job details
- `PUT /api/v1/jobs/{job_id}` - Update job posting
- `DELETE /api/v1/jobs/{job_id}` - Delete job posting

### Candidate Management (`/api/v1/candidates`)

- `POST /api/v1/candidates/evaluate` - Evaluate candidate against job requirements
- `GET /api/v1/candidates` - List all candidates (recruiters/admins only)
- `GET /api/v1/candidates/{candidate_id}` - Get candidate details
- `GET /api/v1/candidates/{candidate_id}/evaluations` - Get all evaluations for a candidate

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `ENV_EXAMPLE.txt` to `.env` and update the values:

```bash
cp ENV_EXAMPLE.txt .env
```

Key variables to set:
- `POSTGRES_URL` - PostgreSQL connection string
- `MONGODB_URL` - MongoDB connection string
- `JWT_SECRET_KEY` - Secret key for JWT tokens (change in production!)

### 3. Set Up Databases

**PostgreSQL:**
```bash
# Create database
createdb campus_connect

# Run migrations
alembic upgrade head
```

**MongoDB:**
```bash
# MongoDB should be running on localhost:27017
# Database will be created automatically on first use
```

### 4. Run the Server

```bash
python start_server.py
# or
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation (Swagger UI) at `http://localhost:8000/docs`

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

To get a token:
1. Register a user: `POST /api/v1/auth/register`
2. Login: `POST /api/v1/auth/login` (returns JWT token)

## Example Usage

### Register and Login

```python
import requests

# Register
response = requests.post("http://localhost:8000/api/v1/auth/register", json={
    "email": "student@example.com",
    "password": "password123",
    "role": "student"
})

# Login
response = requests.post("http://localhost:8000/api/v1/auth/login", data={
    "username": "student@example.com",
    "password": "password123"
})
token = response.json()["access_token"]
```

### Upload Resume

```python
headers = {"Authorization": f"Bearer {token}"}

with open("resume.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/resume/upload",
        files={"file": f},
        headers=headers
    )
resume_id = response.json()["resume_id"]
```

### Search Jobs

```python
response = requests.post(
    "http://localhost:8000/api/v1/student/jobs/search",
    json={
        "query": "I want a backend developer role with Python",
        "student_skills": ["Python", "FastAPI", "PostgreSQL"],
        "top_k": 10
    },
    headers=headers
)
```

## Database Migrations

To create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

To apply migrations:
```bash
alembic upgrade head
```

To rollback:
```bash
alembic downgrade -1
```

## CORS Configuration

CORS is configured to allow requests from:
- `http://localhost:3000` (Next.js client)
- `http://localhost:8000`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:8000`

Update `CORS_ORIGINS` in `config.py` for production.

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

Error responses include a `detail` field with the error message.
