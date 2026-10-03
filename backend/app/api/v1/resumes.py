from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.ai.resume_parser import extract_pdf_text
from app.core.config import settings

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload", status_code=201)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(400, "Please upload a PDF resume.")
    data = await file.read()
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds {settings.max_upload_mb} MB limit.")
    if not data.startswith(b"%PDF"):
        raise HTTPException(400, "The uploaded file is not a valid PDF.")
    try:
        text = extract_pdf_text(data)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    directory = Path(settings.upload_dir); directory.mkdir(parents=True, exist_ok=True)
    safe_name = f"user_{user.id}_{uuid4().hex}.pdf"
    path = directory / safe_name
    path.write_bytes(data)
    resume = Resume(user_id=user.id, original_filename=Path(file.filename).name[:255], storage_path=str(path), extracted_text=text)
    db.add(resume); db.commit(); db.refresh(resume)
    return {"id": resume.id, "filename": resume.original_filename, "uploaded_at": resume.uploaded_at.isoformat()}

@router.get("")
def list_resumes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.uploaded_at.desc()).all()
    return [{"id": r.id, "filename": r.original_filename, "uploaded_at": r.uploaded_at.isoformat()} for r in rows]

@router.delete("/{resume_id}", status_code=204)
def delete_resume(resume_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not row: raise HTTPException(404, "Resume not found.")
    try: Path(row.storage_path).unlink(missing_ok=True)
    except OSError: pass
    db.delete(row); db.commit()
