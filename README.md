# AI Resume Analyzer

An AI-powered full-stack application that analyzes a candidate's resume against a job description and provides an explainable assessment of job fit, matching skills, missing skills, interview readiness, and improvement suggestions.

The project is built using **React, FastAPI, MySQL, SQLAlchemy, Alembic, JWT authentication, Docker, and Google Gemini**.

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Application Flow](#application-flow)
- [AI Analysis Pipeline](#ai-analysis-pipeline)
- [Scoring Approach](#scoring-approach)
- [Authentication Flow](#authentication-flow)
- [Database Design](#database-design)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [API Architecture](#api-architecture)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Docker Architecture](#docker-architecture)
- [Environment Configuration](#environment-configuration)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Security](#security)
- [Engineering Decisions](#engineering-decisions)
- [Challenges Solved](#challenges-solved)
- [Future Improvements](#future-improvements)
- [Interview Explanation](#interview-explanation)
- [Disclaimer](#disclaimer)

---

# Project Overview

The **AI Resume Analyzer** is a full-stack web application designed to help candidates understand how closely their resume matches a particular job description.

Instead of relying only on keyword matching, the application combines structured skill comparison with **Google Gemini** to provide contextual analysis.

The system extracts text from a candidate's PDF resume, accepts a job description, sends the relevant content through the analysis pipeline, and generates a structured result containing:

- Match score
- Matching skills
- Missing skills
- Interview readiness
- Improvement suggestions
- Overall summary

The result is persisted in MySQL so users can review their previous analyses later.

---

# Problem Statement

When applying for jobs, candidates often need to manually compare their resumes against job descriptions.

This process has several problems:

- Important skills can be difficult to identify manually.
- Candidates may not know which required skills are missing.
- Keyword matching alone does not understand context.
- There is no structured explanation for why a resume matches a particular role.
- Previous analysis results are difficult to track.

The goal of this project is to provide a centralized application that automates this comparison and produces an understandable analysis.

---

# Solution

The application provides an end-to-end workflow:

```text
User
 |
 v
Register / Login
 |
 v
Upload Resume
 |
 v
Extract Resume Text
 |
 v
Create / Upload Job Description
 |
 v
Start Analysis
 |
 v
Resume + Job Description
 |
 v
Analysis Service
 |
 +-- Skill comparison
 |
 +-- Gemini contextual assessment
 |
 v
Structured Analysis
 |
 +-- Match Score
 +-- Matching Skills
 +-- Missing Skills
 +-- Interview Readiness
 +-- Suggestions
 +-- Summary
 |
 v
Store Result in MySQL
 |
 v
Display Result in React
 |
 v
Available in Analysis History
```

---

# Key Features

## Authentication

- User registration
- User login
- JWT-based authentication
- Password hashing
- Protected routes
- Authenticated API requests
- Current-user endpoint

## Resume Management

- PDF resume upload
- File validation
- Resume text extraction
- Resume persistence
- Resume listing
- Resume deletion

## Job Description Management

- Create job descriptions manually
- Upload job descriptions from `.txt` files
- Store job descriptions
- Retrieve existing job descriptions

## AI Resume Analysis

The application analyzes:

- Resume content
- Required job skills
- Matching skills
- Missing skills
- Interview readiness
- Improvement suggestions
- Overall candidate-job fit

## Dashboard

The frontend provides a dashboard for accessing:

- Resume information
- Job information
- Analysis history
- Analysis results

## Analysis History

Users can access previous analyses and review:

- Match score
- Skills
- Missing skills
- Readiness
- Suggestions
- Summary

## Docker Support

The complete application can be started using:

```bash
docker compose up --build
```

The environment contains:

- React frontend
- FastAPI backend
- MySQL database

---

# System Architecture

```text
                         +----------------------+
                         |       User           |
                         |      Browser         |
                         +----------+-----------+
                                    |
                                    | HTTP
                                    v
                         +----------------------+
                         |    React Frontend    |
                         |                      |
                         |  React + Vite        |
                         |  React Router        |
                         |  Auth Context        |
                         |  Axios               |
                         +----------+-----------+
                                    |
                                    | REST API
                                    v
                         +----------------------+
                         |    FastAPI Backend   |
                         |                      |
                         | API Routes           |
                         | Authentication       |
                         | Resume Processing    |
                         | Job Management       |
                         | Analysis Service     |
                         +-------+-------+------+
                                 |       |
                        SQLAlchemy|       |Gemini API
                                 |       |
                                 v       v
                         +------------+ +--------------+
                         |   MySQL    | |Google Gemini |
                         |            | |              |
                         | Users      | | AI Analysis  |
                         | Resumes    | +--------------+
                         | Jobs       |
                         | Analyses   |
                         +------------+
```

---

# Application Flow

## 1. User Registration

The user creates an account.

```text
User
 |
 v
Registration Form
 |
 v
FastAPI
 |
 v
Password Hashing
 |
 v
MySQL
```

The password is stored as a hash rather than plain text.

## 2. User Login

```text
Email + Password
       |
       v
FastAPI Authentication
       |
       v
Verify Password
       |
       v
Generate JWT
       |
       v
Frontend
```

The frontend uses the returned access token when accessing protected APIs.

## 3. Resume Upload

```text
PDF Resume
    |
    v
React Upload
    |
    v
FastAPI
    |
    +-- File validation
    |
    +-- PDF processing
    |
    +-- Text extraction
    |
    v
MySQL
```

The extracted resume content is associated with the authenticated user.

## 4. Job Description

The user can either create a job description manually or upload a `.txt` file.

```text
Manual Job Description
          |
          +------------+
                       |
                       v
                 Job Description
                       ^
          +------------+
          |
TXT File Upload
```

The job description is then stored for analysis.

## 5. Resume Analysis

The user selects the relevant resume and job description and starts the analysis.

```text
Resume
  +
Job Description
  |
  v
FastAPI
  |
  v
Analysis Service
  |
  +---------------+
  |               |
  v               v
Skill Analysis   Gemini
  |               |
  +-------+-------+
          |
          v
Structured Result
          |
          v
        MySQL
          |
          v
       React UI
```

---

# AI Analysis Pipeline

The AI pipeline is one of the core components of the project.

```text
                 Resume PDF
                     |
                     v
              PDF Text Parser
                     |
                     v
                Resume Text
                     |
                     v
              Analysis Service
                     ^
                     |
              Job Description
                     |
                     v
                Prompt Builder
                     |
                     v
              Google Gemini
                     |
                     v
           Structured AI Response
                     |
          +----------+-----------+
          |          |           |
          v          v           v
       Matching    Missing    Interview
        Skills      Skills     Readiness
          |          |           |
          +----------+-----------+
                     |
                     v
                Suggestions
                     |
                     v
                  Summary
                     |
                     v
                Match Score
                     |
                     v
                 MySQL
```

---

# AI Components

The backend separates AI-related functionality into dedicated modules.

```text
backend/app/ai/
|
+-- gemini_client.py
+-- job_matcher.py
+-- prompt_templates.py
+-- resume_parser.py
```

### `gemini_client.py`

Responsible for communicating with the Google Gemini API.

### `job_matcher.py`

Contains the resume/job matching logic.

### `prompt_templates.py`

Contains prompts used to guide the AI analysis.

### `resume_parser.py`

Handles extraction of text from uploaded PDF resumes.

This separation keeps the AI functionality modular and easier to maintain.

---

# Scoring Approach

The application provides an explainable match score rather than presenting only an unexplained AI-generated number.

The analysis considers:

```text
Resume
   |
   +-- Required Skills
   |
   +-- Matching Skills
   |
   +-- Missing Skills
          |
          v
   Skill Coverage
          |
          +
   Contextual Gemini Assessment
          |
          v
      Match Score
```

Example:

```text
Match Score: 82

Matching Skills:
- Python
- SQL
- REST APIs
- Docker

Missing Skills:
- AWS
- Kubernetes

Interview Readiness:
Strong backend fundamentals with areas for improvement
in cloud technologies.

Suggestions:
- Improve AWS knowledge
- Add cloud deployment experience
- Highlight REST API projects
```

The score is intended to help users understand their alignment with a job description and should not be treated as an automated hiring decision.

---

# Authentication Flow

The application uses JWT authentication.

```text
                 +---------------+
                 |     User      |
                 +-------+-------+
                         |
                         v
                  Login/Register
                         |
                         v
                FastAPI Auth API
                         |
                         v
                 Password Verify
                         |
                         v
                    JWT Token
                         |
                         v
                  React Frontend
                         |
                         v
               Authorization Header
                         |
                         v
                Protected FastAPI
                     Endpoints
```

Example:

```http
Authorization: Bearer <access_token>
```

Protected APIs verify the token before processing the request.

---

# Database Design

The application uses **MySQL** with **SQLAlchemy ORM**.

```text
+--------------+
|    Users     |
+------+-------+
       |
       | 1:N
       v
+--------------+
|   Resumes    |
+------+-------+
       |
       |
       v
+--------------+       +---------------------+
|   Analyses   |<------| Job Descriptions    |
+--------------+       +---------------------+
```

## Users

Stores user authentication information.

Typical data includes:

- ID
- Name
- Email
- Password hash

## Resumes

Stores uploaded resume information and extracted text.

## Job Descriptions

Stores job descriptions created or uploaded by users.

## Analyses

Stores the output of the resume/job analysis.

Important fields include:

- `match_score`
- `matching_skills`
- `missing_skills`
- `interview_readiness`
- `suggestions`
- `summary`
- `status`
- `created_at`

---

# Database Migrations

The project uses **Alembic** for database schema management.

Migration files are stored under:

```text
backend/alembic/
```

Alembic allows database schema changes to be version-controlled instead of relying only on manual database modifications.

---

# Backend Architecture

The backend follows a layered structure.

```text
                 FastAPI Request
                       |
                       v
                  API Router
                       |
                       v
               API Dependencies
                       |
                       v
                Service Layer
                       |
             +---------+---------+
             |                   |
             v                   v
       Resume Parser        Analysis Service
                                   |
                                   v
                              Gemini Client
                       |
                       v
                  SQLAlchemy ORM
                       |
                       v
                     MySQL
```

This separation keeps:

- API logic
- business logic
- AI logic
- database logic

from becoming tightly coupled.

---

# Backend Project Structure

```text
backend/
|
+-- app/
|   |
|   +-- ai/
|   |   +-- __init__.py
|   |   +-- gemini_client.py
|   |   +-- job_matcher.py
|   |   +-- prompt_templates.py
|   |   +-- resume_parser.py
|   |
|   +-- api/
|   |   +-- __init__.py
|   |   +-- deps.py
|   |   |
|   |   +-- v1/
|   |       +-- __init__.py
|   |       +-- analyses.py
|   |       +-- auth.py
|   |       +-- dashboard.py
|   |       +-- jobs.py
|   |       +-- resumes.py
|   |       +-- router.py
|   |
|   +-- core/
|   |   +-- __init__.py
|   |   +-- config.py
|   |   +-- security.py
|   |
|   +-- db/
|   |   +-- __init__.py
|   |   +-- session.py
|   |
|   +-- models/
|   |   +-- __init__.py
|   |   +-- analysis.py
|   |   +-- job.py
|   |   +-- resume.py
|   |   +-- user.py
|   |
|   +-- schemas/
|   |   +-- __init__.py
|   |   +-- analysis.py
|   |   +-- auth.py
|   |   +-- job.py
|   |
|   +-- services/
|   |   +-- __init__.py
|   |   +-- analysis_service.py
|   |
|   +-- main.py
|
+-- alembic/
+-- tests/
+-- uploads/
+-- Dockerfile
+-- requirements.txt
+-- alembic.ini
```

---

# Frontend Architecture

The frontend is built with React and Vite.

```text
                    React Application
                           |
              +------------+------------+
              |            |            |
              v            v            v
         AuthContext    React Router   API Service
              |            |            |
              |            |            v
              |            |         FastAPI
              |            |
              v            v
        Authentication   Application Pages
```

The frontend contains:

- Authentication
- Dashboard
- Resume upload
- Job description management
- Analysis
- Results
- History

---

# Frontend Project Structure

```text
frontend/
|
+-- src/
|   |
|   +-- components/
|   |   +-- Layout.jsx
|   |   +-- ProtectedRoute.jsx
|   |
|   +-- context/
|   |   +-- AuthContext.jsx
|   |
|   +-- pages/
|   |   +-- Analyze.jsx
|   |   +-- Auth.jsx
|   |   +-- Dashboard.jsx
|   |   +-- History.jsx
|   |   +-- Results.jsx
|   |
|   +-- services/
|   |   +-- api.js
|   |
|   +-- App.jsx
|   +-- main.jsx
|   +-- styles.css
|
+-- Dockerfile
+-- index.html
+-- package.json
```

---

# API Architecture

The backend exposes REST APIs under:

```text
/api/v1
```

## Authentication APIs

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

## Resume APIs

```http
POST   /api/v1/resumes/upload
GET    /api/v1/resumes
DELETE /api/v1/resumes/{id}
```

## Job APIs

```http
POST /api/v1/jobs
POST /api/v1/jobs/upload
GET  /api/v1/jobs
```

## Analysis APIs

```http
POST /api/v1/analyses
GET  /api/v1/analyses
GET  /api/v1/analyses/{id}
```

## Dashboard API

```http
GET /api/v1/dashboard
```

---

# Project Structure

```text
AI-Resume-Analyzer/
|
+-- backend/
|   +-- app/
|   +-- alembic/
|   +-- tests/
|   +-- uploads/
|   +-- .env.example
|   +-- Dockerfile
|   +-- alembic.ini
|   +-- requirements.txt
|
+-- frontend/
|   +-- src/
|   +-- .env.example
|   +-- Dockerfile
|   +-- index.html
|   +-- package.json
|
+-- .env.example
+-- .gitignore
+-- docker-compose.yml
+-- README.md
```

---

# Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Build Tool | Vite |
| Routing | React Router |
| API Client | Axios |
| Backend | FastAPI |
| Programming Language | Python 3.11 |
| Validation | Pydantic |
| ORM | SQLAlchemy |
| Database | MySQL 8.4 |
| Database Migration | Alembic |
| Authentication | JWT |
| Password Security | Password Hashing |
| AI | Google Gemini |
| PDF Processing | PyPDF |
| Testing | Pytest |
| Containerization | Docker |
| Orchestration | Docker Compose |

---

# Docker Architecture

Docker Compose runs the application as multiple services.

```text
                 Docker Compose
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
   +---------+   +---------+   +---------+
   |Frontend |   | Backend |   |  MySQL  |
   |         |   |         |   |         |
   | React   |-->| FastAPI |-->| MySQL   |
   | Vite    |   | Python  |   |  8.4    |
   +---------+   +---------+   +---------+
      :5173         :8000         :3307
```

### Services

| Service | Purpose | Port |
|---|---|---|
| frontend | React/Vite application | 5173 |
| backend | FastAPI API | 8000 |
| db | MySQL database | 3307 |

---

# Environment Configuration

Environment variables are used for configuration and secrets.

Example root `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
JWT_SECRET_KEY=replace_with_a_random_secret
```

Backend configuration can be provided through:

```text
backend/.env
```

Frontend configuration:

```text
frontend/.env.local
```

Example:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Security Note

Never commit real credentials to GitHub.

Do not commit:

```text
.env
backend/.env
frontend/.env
```

Only example configuration files containing placeholders should be committed.

---

# Running the Project

## Prerequisites

Recommended:

- Docker Desktop
- Docker Compose
- Google Gemini API key

For local development without Docker:

- Python 3.11+
- Node.js 20+
- MySQL

---

# Run with Docker

## Step 1: Clone the repository

```bash
git clone https://github.com/Raghupathy-23/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

## Step 2: Create environment file

Copy:

```text
.env.example
```

to:

```text
.env
```

Then configure:

```env
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET_KEY=your_random_secret
```

Do not commit this file.

## Step 3: Start the application

```bash
docker compose up --build
```

## Step 4: Access the application

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:8000
```

FastAPI Swagger:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

---

# Local Development Without Docker

## Backend

Navigate to:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scriptsctivate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure:

```text
backend/.env
```

Then run:

```bash
uvicorn app.main:app --reload
```

---

# Frontend

Navigate to:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Configure:

```text
frontend/.env.local
```

Example:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

This allows developers to:

- View available endpoints
- Inspect request schemas
- Test APIs
- View response schemas
- Test authentication-protected endpoints

---

# Testing

Backend tests are located under:

```text
backend/tests/
```

Run:

```bash
cd backend
pytest
```

The project currently includes tests for the job-matching functionality.

---

# Error Handling

The application validates data at multiple layers.

```text
React
  |
  v
FastAPI Request Validation
  |
  v
Pydantic
  |
  v
Service Layer
  |
  v
SQLAlchemy
  |
  v
MySQL
```

Examples of validation include:

- Invalid authentication credentials
- Invalid file types
- Invalid uploaded resumes
- Missing request fields
- Unauthorized API requests
- Invalid database relationships

---

# Security

The project implements basic security practices suitable for an MVP.

### Password Security

Passwords are hashed before being stored.

```text
Plain Password
      |
      v
Password Hashing
      |
      v
Database
```

### JWT Authentication

Authenticated requests use JWT access tokens.

### Environment Variables

Sensitive values such as:

- Gemini API keys
- JWT secrets
- Database credentials

are kept outside the source code.

### Protected Routes

Frontend protected routes prevent unauthenticated users from accessing authenticated pages.

Backend protected endpoints verify the JWT token.

---

# Engineering Decisions

## Why FastAPI?

FastAPI was selected because it provides:

- Automatic OpenAPI documentation
- Request validation
- Dependency injection
- Good performance
- Python ecosystem compatibility
- Easy integration with AI/ML libraries

## Why React?

React provides:

- Component-based development
- Reusable UI components
- Client-side routing
- Interactive analysis results
- Straightforward API integration

## Why MySQL?

The application contains relational data such as:

```text
User
  +-- Resumes
  +-- Job Descriptions
  +-- Analyses
```

A relational database is therefore suitable for maintaining these relationships.

## Why SQLAlchemy?

SQLAlchemy provides:

- ORM abstraction
- Relationship management
- Query support
- Integration with FastAPI
- Database portability

## Why Alembic?

Alembic allows database schema changes to be version controlled and deployed consistently.

## Why Gemini?

Resume analysis requires contextual understanding rather than only exact keyword matching.

Gemini is used for contextual AI analysis of resume and job-description content.

---

# Challenges Solved

## 1. PDF Resume Processing

The system converts uploaded PDF resumes into text that can be analyzed.

```text
PDF
 |
 v
PyPDF
 |
 v
Extracted Text
 |
 v
Analysis Pipeline
```

## 2. AI Response Integration

The AI response needs to be converted into structured application data.

The backend separates AI interaction from the API layer using dedicated AI and service modules.

## 3. Authentication

The application requires authenticated users to access private resume and analysis data.

JWT authentication and password hashing are used to address this.

## 4. Frontend/Backend Integration

The React frontend communicates with FastAPI through REST APIs.

```text
React
 |
 | Axios
 v
FastAPI
 |
 v
MySQL
```

## 5. Database Schema Management

Alembic is used to manage database schema changes rather than relying only on manual SQL changes.

## 6. Containerized Development

Docker Compose allows the frontend, backend, and database to run together with consistent configuration.

---

# Production Improvements

The current implementation is an MVP. A production deployment could introduce the following improvements.

## Authentication

- Email verification
- Password reset
- Refresh token rotation
- Session management
- Multi-factor authentication

## File Processing

- Malware scanning
- Private object storage
- File encryption
- File retention policies
- Automatic deletion

## AI Processing

- Background workers
- Redis/Celery or another task queue
- Retry handling
- LLM response validation
- Prompt versioning
- AI evaluation datasets
- Response caching

## Infrastructure

- Managed MySQL/PostgreSQL
- Object storage
- CI/CD
- Reverse proxy
- HTTPS
- Application monitoring
- Centralized logging

## Scalability

The synchronous AI analysis can be moved to a background processing architecture:

```text
User
 |
 v
React
 |
 v
FastAPI
 |
 v
Task Queue
 |
 v
AI Worker
 |
 v
Gemini
 |
 v
Database
 |
 v
React polls / receives result
```

This prevents long-running AI requests from blocking API requests.

---

# Future Architecture

A scalable version could look like:

```text
                         +--------------+
                         |    React     |
                         |   Frontend   |
                         +------+-------+
                                |
                                v
                         +--------------+
                         |   FastAPI    |
                         |     API      |
                         +------+-------+
                                |
                +---------------+---------------+
                |               |               |
                v               v               v
          +----------+    +----------+    +----------+
          | MySQL    |    |  Redis   |    | Storage  |
          |          |    |  Queue   |    |          |
          +----------+    +----+-----+    +----------+
                               |
                               v
                         +--------------+
                         |  AI Worker   |
                         +------+-------+
                                |
                                v
                         +--------------+
                         | Gemini API   |
                         +--------------+
```

---

# Interview Explanation

A concise way to explain the project in an interview:

> **"I built a full-stack AI Resume Analyzer using React, FastAPI, MySQL, SQLAlchemy, Alembic, JWT authentication, and Google Gemini. The application allows users to register, upload a PDF resume, create or upload a job description, and analyze the match between them.**
>
> **On the backend, FastAPI handles authentication, file uploads, job management, and analysis APIs. I separated the AI logic into dedicated modules for PDF parsing, prompt construction, Gemini communication, and job matching. SQLAlchemy handles database access and Alembic manages schema migrations.**
>
> **For the analysis, the system extracts resume text, combines it with the job description, performs structured skill comparison, and uses Gemini for contextual assessment. The resulting match score, matching skills, missing skills, interview readiness, suggestions, and summary are stored in MySQL and displayed through the React frontend.**
>
> **The application is containerized with Docker Compose, with separate frontend, backend, and MySQL services. I also implemented JWT authentication, password hashing, protected routes, API validation, and analysis history."**

---

# What This Project Demonstrates

This project demonstrates practical experience with:

- Full-stack web development
- React
- Vite
- FastAPI
- REST API design
- Python
- Pydantic
- SQLAlchemy
- MySQL
- Alembic
- JWT authentication
- Password hashing
- PDF processing
- Google Gemini API
- Prompt engineering
- AI-assisted semantic analysis
- Explainable scoring
- File uploads
- Docker
- Docker Compose
- Pytest
- Git and GitHub
- Frontend/backend integration
- Database design

---

# Project Goals

The main goals of this project are:

1. Automate resume-to-job comparison.
2. Provide an understandable skill gap analysis.
3. Use AI for contextual rather than purely keyword-based analysis.
4. Store analysis history for future reference.
5. Demonstrate a production-oriented full-stack architecture.
6. Provide a foundation that can be extended into a scalable AI recruitment-support platform.

---

# Disclaimer

This application is designed as a resume analysis and career-support tool.

AI-generated scores, assessments, and recommendations are estimates and should not be treated as automated hiring decisions.

Users should review AI-generated results alongside the original resume and job description.
