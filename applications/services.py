import json
import os

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
from django.conf import settings

load_dotenv()


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY") or getattr(settings, "OPENAI_API_KEY", None)

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment or Django settings.")

    return OpenAI(api_key=api_key)


def analyze_resume_vs_job(resume_text: str, job_description: str) -> dict:
    client = get_openai_client()

    prompt = f"""
You are a technical resume analysis assistant.

Compare the candidate resume to the job description and return JSON only.

Return this exact structure:
{{
  "job_title_guess": "",
  "seniority_level": "",
  "required_skills": [],
  "preferred_skills": [],
  "resume_strengths": [],
  "missing_or_weak_skills": [],
  "match_score": 0,
  "fit_assessment": "",
  "tailored_resume_suggestions": []
}}

Rules:
- "match_score" must be an integer from 0 to 100.
- Only return valid JSON.
- Be realistic, not overly generous.
- Base the analysis only on the provided resume and job description.

Resume:
{resume_text}

Job Description:
{job_description}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
    except RateLimitError:
        raise ValueError(
            "OpenAI API quota/billing issue: check your billing setup and available credits."
        )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{content}")