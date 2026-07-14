from .core import ask_ai

def email_generator(candidate_name: str, email_type: str, context: str = "") -> str:
    system = (
        "You are an expert HR Communications Specialist and Talent Acquisition Leader. "
        "Your task is to draft highly professional, warm, engaging, and polished corporate emails. "
        "Each email must feature clear headings, a proper greeting, a structured body with clear key points if necessary, "
        "and a professional closing signature. Do not include placeholders—use realistic, polished details. "
        "Maintain a friendly yet highly business-professional tone throughout."
    )
    prompt = (
        f"Candidate Name: {candidate_name}\n"
        f"Email Type: {email_type}\n"
        f"Additional Context/Details:\n{context}\n\n"
        f"Generate a complete, high-quality, professional email body suitable for sending to the candidate."
    )
    return ask_ai(prompt, system)
