from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()    



# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Read Resume
reader = PdfReader("Raghupathy(DA_resume).pdf")

resume_text = ""

for page in reader.pages:
    resume_text += page.extract_text()
with open("job_description.txt", "r") as file:
    job_description = file.read()

prompt = f"""
You are an expert recruiter.

Compare the resume and job description.

Return ONLY valid JSON.

Format:

{{
  "match_score": 0,
  "matching_skills": [],
  "missing_skills": [],
  "interview_readiness": "",
  "suggestions": []
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # Convert JSON string into Python dictionary
    cleaned = (
    response.text
    .replace("```json", "")
    .replace("```", "")
    .strip()
)
    result = json.loads(cleaned)

    # Save output
    with open("analysis.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    print("\n===== Resume Analysis =====")
    print(f"Match Score : {result['match_score']}%")

    print("\nMatching Skills")
    for skill in result["matching_skills"]:
        print(f"✓ {skill}")

    print("\nMissing Skills")
    for skill in result["missing_skills"]:
        print(f"✗ {skill}")

    print("\nInterview Readiness")
    print(result["interview_readiness"])

    print("\nSuggestions")
    for suggestion in result["suggestions"]:
        print(f"• {suggestion}")

except Exception as e:
    print("Error:", e)
