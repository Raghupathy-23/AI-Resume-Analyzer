from pydantic import BaseModel, Field, ConfigDict

class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    company: str = Field(default="", max_length=180)
    description: str = Field(min_length=20, max_length=30000)

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    description: str
    created_at: str
    model_config = ConfigDict(from_attributes=True)
