from .core import ask_ai

def hiring_recommendation(candidate_name: str, match_pct: float, experience: float, grade: str, gaps: str) -> str:
    system = "You are a recruitment decision support specialist. Provide a detailed, concise hiring recommendation and reasoning based on the candidate's metrics and gaps."
    prompt = f"Candidate: {candidate_name}\nMatch Score: {match_pct}%\nExperience: {experience} years\nGrade: {grade}\nGaps Identified: {gaps}\n\nProvide decision support reasoning."
    return ask_ai(prompt, system)
