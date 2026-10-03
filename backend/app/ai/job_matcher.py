import re

def normalize_skill(skill: str) -> str:
    return re.sub(r"[^a-z0-9+#.]", "", skill.lower())

def deterministic_skill_match(resume_text: str, job_description: str):
    # A compact starter vocabulary; expand and maintain this list as the product grows.
    vocabulary = [
        "Python", "SQL", "MySQL", "PostgreSQL", "Git", "REST API", "FastAPI",
        "Docker", "AWS", "React", "JavaScript", "Java", "Django", "Linux",
        "Machine Learning", "Pandas", "NumPy", "Azure", "GCP"
    ]
    resume_norm = normalize_skill(resume_text)
    job_norm = normalize_skill(job_description)
    required = [s for s in vocabulary if normalize_skill(s) in job_norm]
    matched = [s for s in required if normalize_skill(s) in resume_norm]
    missing = [s for s in required if s not in matched]
    coverage = round((len(matched) / len(required)) * 100) if required else 0
    return required, matched, missing, coverage

def calculate_score(skill_coverage: int, context_score: int) -> int:
    # Initial explainable weighting: 60% required-skill coverage, 40% contextual relevance.
    return max(0, min(100, round(skill_coverage * 0.60 + context_score * 0.40)))
