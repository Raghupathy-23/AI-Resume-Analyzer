# AI Resume Analyzer

A full-stack resume-to-job matching application built with React, FastAPI, MySQL, SQLAlchemy, Alembic, and Google Gemini.

## Features
- Register/login with JWT authentication and hashed passwords
- Upload PDF resumes with validation and text extraction
- Create job descriptions manually or from `.txt` files
- AI-assisted resume/job analysis with matching skills, missing skills, readiness, and suggestions
- Explainable score combining skill coverage with contextual Gemini assessment
- Persist resumes, jobs, and analysis history in MySQL
- React dashboard, upload/analyze flow, result view, and history
- Docker Compose for local development

## Requirements
- Docker Desktop + Docker Compose (recommended), or Python 3.11+ and Node.js 20+
- Google Gemini API key for AI analysis

## Quick start (Docker)
1. Copy `.env.example` to `.env` in the project root.
2. Set `GEMINI_API_KEY` in `.env`. The app can start without it, but analysis requires it.
3. Run:
   ```bash
   docker compose up --build
   ```
4. Open the frontend at http://localhost:5173 and API docs at http://localhost:8000/docs.

The API waits for MySQL to become healthy and creates the tables at startup for this MVP.

## Local development (without Docker)
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Set DATABASE_URL and GEMINI_API_KEY in backend/.env (see backend/.env.example)
uvicorn app.main:app --reload
```
### Frontend
```bash
cd frontend
npm install
npm run dev
```
Set `VITE_API_URL=http://localhost:8000/api/v1` in `frontend/.env.local`.

## Main API
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/resumes/upload`
- `GET /api/v1/resumes`
- `DELETE /api/v1/resumes/{id}`
- `POST /api/v1/jobs`
- `POST /api/v1/jobs/upload`
- `GET /api/v1/jobs`
- `POST /api/v1/analyses`
- `GET /api/v1/analyses`
- `GET /api/v1/analyses/{id}`
- `GET /api/v1/dashboard`

## Notes
- Uploaded files are stored in `backend/uploads/` during local development. Do not expose this directory publicly in production.
- This tool provides career guidance, not a hiring decision. Scores are estimates and should be reviewed alongside the resume.
- For production, add email verification/password reset, refresh-token rotation, rate limiting, malware scanning, private object storage, retention/deletion workflows, and managed database backups.
- The current MVP uses local file storage and synchronous AI requests. Add a background queue for large workloads.
