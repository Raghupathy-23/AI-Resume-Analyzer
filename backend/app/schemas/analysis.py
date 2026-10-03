from pydantic import BaseModel, Field, ConfigDict

class AnalysisCreate(BaseModel):
    resume_id: int
    job_description_id: int

class AnalysisOut(BaseModel):
    id: int
    resume_id: int
    job_description_id: int
    match_score: int
    matching_skills: list[str]
    missing_skills: list[str]
    interview_readiness: str
    suggestions: list[str]
    summary: str
    status: str
    created_at: str
    model_config = ConfigDict(from_attributes=True)
