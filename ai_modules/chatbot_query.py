from .core import ask_ai

def chatbot_query(user_query: str, candidates_context: str, resume_context: str = None) -> str:
    system_rules = [
        "You are the AI assistant for the 'AI Recruitment & Talent Copilot' project only.",
        "Your responses are strictly scoped to the following project-related topics:",
        "- Candidates in the current pool",
        "- Job roles and requirements",
        "- Match scores",
        "- Shortlisting and candidate fit",
        "- Interview scheduling",
        "- Hiring recommendations and recruiter decisions",
        "- Organizational talent/performance summaries",
        "- How the features of this app work."
    ]
    
    if resume_context:
        system_rules.append("Additionally, a candidate resume has been uploaded. You may answer questions about THAT specific resume's content (skills, experience, suitability for a role).")
        prompt = (
            f"Candidates Summary Table:\n{candidates_context}\n\n"
            f"Uploaded Resume Content:\n{resume_context}\n\n"
            f"User Query: {user_query}"
        )
    else:
        prompt = (
            f"Candidates Summary Table:\n{candidates_context}\n\n"
            f"User Query: {user_query}"
        )

    system_rules.extend([
        "If the user query is outside this scope (e.g., general knowledge, general coding help, personal questions, history, current events, etc.), you must NOT simply refuse.",
        "Instead, write a short, specific, helpful redirect in your own words:",
        "1. Acknowledge that the query is outside your recruitment scope.",
        "2. Briefly specify what you are designed to help with (mentioning the candidates list, job roles, features, or the uploaded resume if present).",
        "3. Provide 1 or 2 concrete, relevant example questions the user could ask instead related to the project/uploaded resume."
    ])
    
    system = "\n".join(system_rules)
    return ask_ai(prompt, system, num_predict=150)
