from .core import ask_ai

def talent_insight(avg_match_by_role: dict, experience_band_distribution: dict) -> str:
    system = "You are an organizational development expert. Analyze macro-level company talent metrics and generate talent insights."
    prompt = f"Average Match Score by Role: {avg_match_by_role}\nExperience Band Distribution: {experience_band_distribution}\n\nProvide organizational talent insights."
    return ask_ai(prompt, system)
