from .core import ask_ai

def recruitment_analysis(total_openings: int, total_applicants: int, total_shortlisted: int, role_counts: dict) -> str:
    system = "You are a recruiting director analyzing pipeline operations metrics. Provide data-driven, structured, and complete executive recommendations and insights."
    prompt = f"Active Openings: {total_openings}\nTotal Applicants: {total_applicants}\nTotal Shortlisted: {total_shortlisted}\nApplicants per role: {role_counts}\n\nGenerate a complete executive recruitment insight report."
    return ask_ai(prompt, system, num_predict=2048)

