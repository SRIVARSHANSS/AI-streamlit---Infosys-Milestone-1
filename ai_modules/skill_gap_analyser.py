import json
from .core import ask_ai

def skill_gap_analyser(candidate_skills: list, required_skills: list, experience_years: float, min_experience: int) -> str:
    system = (
        "You are a Senior Talent Acquisition Specialist with 15 years of experience. "
        "Analyze the candidate's skills and experience against the job requirements. "
        "Return ONLY a raw JSON object (no markdown, no code blocks, no explanation) with this exact structure:\n"
        "{\n"
        '  "hire_readiness_score": <integer 0-100>,\n'
        '  "hire_readiness_label": "<one of: Exceptional Match | Strong Match | Moderate Match | Needs Development | Not Ready>",\n'
        '  "experience_assessment": "<one concise sentence about experience fit>",\n'
        '  "key_strengths": [\n'
        '    {"skill": "<skill name>", "note": "<why this is valuable for the role>"}\n'
        "  ],\n"
        '  "growth_areas": [\n'
        '    {\n'
        '      "skill": "<missing skill>",\n'
        '      "severity": "<one of: Critical | High | Medium | Low>",\n'
        '      "gap_note": "<why this skill matters for the role>",\n'
        '      "recommendation": "<specific course, certification or project to bridge the gap>",\n'
        '      "time_to_bridge": "<estimated time e.g. 2-3 weeks>"\n'
        "    }\n"
        "  ],\n"
        '  "overall_recommendation": "<2-3 sentence recruiter verdict on hiring this candidate>"\n'
        "}"
    )
    prompt = (
        f"Candidate Skills: {candidate_skills}\n"
        f"Required Skills: {required_skills}\n"
        f"Candidate Experience: {experience_years} years\n"
        f"Required Minimum Experience: {min_experience} years\n\n"
        "Provide a comprehensive, actionable skill gap analysis for the recruiter."
    )
    return ask_ai(prompt, system)
