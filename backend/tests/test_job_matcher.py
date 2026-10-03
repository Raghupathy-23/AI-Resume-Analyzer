from app.ai.job_matcher import deterministic_skill_match, calculate_score

def test_skill_match():
    required, matched, missing, coverage = deterministic_skill_match(
        "Python, SQL, Git and REST API project experience",
        "Required Skills: Python, SQL, Git, REST API, Docker, AWS"
    )
    assert set(required) == {"Python", "SQL", "Git", "REST API", "Docker", "AWS"}
    assert set(matched) == {"Python", "SQL", "Git", "REST API"}
    assert set(missing) == {"Docker", "AWS"}
    assert coverage == 67

def test_score_is_bounded():
    assert calculate_score(100, 100) == 100
    assert calculate_score(0, 0) == 0
