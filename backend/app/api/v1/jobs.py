from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.job import JobDescription
from app.schemas.job import JobCreate

router = APIRouter(prefix="/jobs", tags=["Job descriptions"])

@router.post("", status_code=201)
def create_job(payload: JobCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row = JobDescription(user_id=user.id, title=payload.title.strip(), company=payload.company.strip(), description=payload.description.strip())
    db.add(row); db.commit(); db.refresh(row)
    return {"id": row.id, "title": row.title, "company": row.company, "description": row.description, "created_at": row.created_at.isoformat()}

@router.post("/upload", status_code=201)
async def upload_job(file: UploadFile = File(...), title: str = Form(...), company: str = Form(""), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(400, "Please upload a .txt job description.")
    raw = await file.read()
    if len(raw) > 100_000: raise HTTPException(413, "Job description is too large.")
    try: description = raw.decode("utf-8").strip()
    except UnicodeDecodeError: raise HTTPException(400, "Text file must use UTF-8 encoding.")
    if len(description) < 20: raise HTTPException(400, "Job description must contain at least 20 characters.")
    return create_job(JobCreate(title=title, company=company, description=description), db, user)

@router.get("")
def list_jobs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.query(JobDescription).filter(JobDescription.user_id == user.id).order_by(JobDescription.created_at.desc()).all()
    return [{"id": r.id, "title": r.title, "company": r.company, "description": r.description, "created_at": r.created_at.isoformat()} for r in rows]

@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row = db.query(JobDescription).filter(JobDescription.id == job_id, JobDescription.user_id == user.id).first()
    if not row: raise HTTPException(404, "Job description not found.")
    db.delete(row); db.commit()
