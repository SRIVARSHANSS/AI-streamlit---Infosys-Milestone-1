from .core import ask_ai

def candidate_ranking(candidates_summary: str, job_description: str) -> str:
    system = "You are a senior recruitment officer. Rank the provided list of candidates for the role based on skills, experience, and match scores. Provide clear ranking rationale."
    prompt = f"Candidates Pool:\n{candidates_summary}\n\nJob Requirements:\n{job_description}\n\nRank the candidates and give the rationale."
    return ask_ai(prompt, system)
