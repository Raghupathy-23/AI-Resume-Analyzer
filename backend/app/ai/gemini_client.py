import json
from google import genai
from app.core.config import settings
from app.ai.prompt_templates import build_analysis_prompt

class AIConfigurationError(RuntimeError):
    pass

def analyze_with_gemini(resume_text: str, job_description: str) -> dict:
    if not settings.gemini_api_key:
        raise AIConfigurationError("GEMINI_API_KEY is not configured on the backend.")
    client = genai.Client(api_key=settings.gemini_api_key)
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=build_analysis_prompt(resume_text, job_description),
        config={"response_mime_type": "application/json", "temperature": 0.1},
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned invalid JSON.") from exc
    if not isinstance(data, dict):
        raise RuntimeError("Gemini response must be a JSON object.")
    return data
