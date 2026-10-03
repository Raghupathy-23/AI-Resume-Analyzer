from app.ai.gemini_client import analyze_with_gemini
from app.ai.job_matcher import deterministic_skill_match, calculate_score

def run_analysis(resume_text: str, job_description: str) -> dict:
    required, matched, missing, coverage = deterministic_skill_match(resume_text, job_description)
    ai = analyze_with_gemini(resume_text, job_description)
    context_score = ai.get("context_score", 50)
    if not isinstance(context_score, int):
        context_score = 50
    context_score = max(0, min(100, context_score))
    ai_matched = ai.get("matching_skills", [])
    ai_missing = ai.get("missing_skills", [])
    suggestions = ai.get("suggestions", [])
    if not isinstance(ai_matched, list): ai_matched = []
    if not isinstance(ai_missing, list): ai_missing = []
    if not isinstance(suggestions, list): suggestions = []
    # Preserve deterministic required-skill evidence and add useful contextual skills from AI.
    final_matched = list(dict.fromkeys(matched + [str(x)[:100] for x in ai_matched[:20]]))
    final_missing = list(dict.fromkeys(missing + [str(x)[:100] for x in ai_missing[:20] if normalize_not_in(x, matched)]))
    return {
        "match_score": calculate_score(coverage, context_score),
        "matching_skills": final_matched[:30],
        "missing_skills": final_missing[:30],
        "interview_readiness": str(ai.get("interview_readiness", "Review the detailed skill gaps."))[:500],
        "suggestions": [str(x)[:500] for x in suggestions[:10]],
        "summary": str(ai.get("summary", ""))[:2000],
    }

def normalize_not_in(skill, matched):
    from app.ai.job_matcher import normalize_skill
    return normalize_skill(str(skill)) not in {normalize_skill(x) for x in matched}
