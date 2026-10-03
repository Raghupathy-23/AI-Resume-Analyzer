from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.job import JobDescription
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate
from app.services.analysis_service import run_analysis

router = APIRouter(prefix="/analyses", tags=["Analysis"])

def serialize(row):
    return {"id": row.id, "resume_id": row.resume_id, "job_description_id": row.job_description_id,
            "match_score": row.match_score, "matching_skills": row.matching_skills or [],
            "missing_skills": row.missing_skills or [], "interview_readiness": row.interview_readiness,
            "suggestions": row.suggestions or [], "summary": row.summary or "", "status": row.status,
            "created_at": row.created_at.isoformat()}

@router.post("", status_code=201)
def create_analysis(payload: AnalysisCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id, Resume.user_id == user.id).first()
    job = db.query(JobDescription).filter(JobDescription.id == payload.job_description_id, JobDescription.user_id == user.id).first()
    if not resume: raise HTTPException(404, "Resume not found.")
    if not job: raise HTTPException(404, "Job description not found.")
    try:
        result = run_analysis(resume.extracted_text, job.description)
    except Exception as exc:
        raise HTTPException(502, f"Analysis could not be completed: {str(exc)[:300]}")
    row = Analysis(user_id=user.id, resume_id=resume.id, job_description_id=job.id, **result)
    db.add(row); db.commit(); db.refresh(row)
    return serialize(row)

@router.get("")
def list_analyses(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.query(Analysis).filter(Analysis.user_id == user.id).order_by(Analysis.created_at.desc()).all()
    return [serialize(r) for r in rows]

@router.get("/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == user.id).first()
    if not row: raise HTTPException(404, "Analysis not found.")
    return serialize(row)
