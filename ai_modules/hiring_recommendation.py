from .core import ask_ai

def hiring_recommendation(candidate_name: str, match_pct: float, experience: float, grade: str, gaps: str) -> str:
    system = "You are a recruitment decision support specialist. Provide a structured, complete, and fully finished hiring recommendation with detailed reasoning based on candidate metrics."
    prompt = f"Candidate: {candidate_name}\nMatch Score: {match_pct}%\nExperience: {experience} years\nGrade: {grade}\nGaps Identified: {gaps}\n\nProvide complete decision support reasoning."
    return ask_ai(prompt, system, num_predict=2048)

