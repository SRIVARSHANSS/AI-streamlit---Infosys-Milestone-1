from .core import ask_ai

def recruitment_analysis(total_openings: int, total_applicants: int, total_shortlisted: int, role_counts: dict) -> str:
    system = "You are a recruiting director analyzing pipeline operations metrics. Provide concise, data-driven recommendations and insight."
    prompt = f"Active Openings: {total_openings}\nTotal Applicants: {total_applicants}\nTotal Shortlisted: {total_shortlisted}\nApplicants per role: {role_counts}\n\nGenerate a brief executive recruitment insight report."
    return ask_ai(prompt, system)
