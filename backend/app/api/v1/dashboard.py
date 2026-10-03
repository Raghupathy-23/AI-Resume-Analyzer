from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.job import JobDescription
from app.models.analysis import Analysis

router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    count_resumes = db.query(func.count(Resume.id)).filter(Resume.user_id == user.id).scalar() or 0
    count_jobs = db.query(func.count(JobDescription.id)).filter(JobDescription.user_id == user.id).scalar() or 0
    count_analyses = db.query(func.count(Analysis.id)).filter(Analysis.user_id == user.id).scalar() or 0
    average = db.query(func.avg(Analysis.match_score)).filter(Analysis.user_id == user.id).scalar()
    recent = db.query(Analysis).filter(Analysis.user_id == user.id).order_by(Analysis.created_at.desc()).limit(5).all()
    return {"resume_count": count_resumes, "job_count": count_jobs, "analysis_count": count_analyses,
            "average_match_score": round(float(average), 1) if average is not None else 0,
            "recent_analyses": [{"id": r.id, "match_score": r.match_score, "created_at": r.created_at.isoformat()} for r in recent]}
