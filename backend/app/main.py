from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.models import User, Resume, JobDescription, Analysis
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # MVP convenience; use Alembic for controlled production migrations.
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router, prefix=settings.api_prefix)

@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
