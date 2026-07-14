from .core import ask_ai

def resume_matching(resume_text: str, job_description: str) -> str:
    system = "You are a professional screening assistant. Provide a structured, concise match summary of the candidate's resume against the job description."
    prompt = f"Resume Summary:\n{resume_text}\n\nJob Description Requirements:\n{job_description}\n\nAnalyze how well the candidate matches the job and provide a summary."
    return ask_ai(prompt, system)
