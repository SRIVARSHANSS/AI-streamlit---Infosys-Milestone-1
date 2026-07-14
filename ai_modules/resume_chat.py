from .core import ask_ai

def resume_chat(candidate_context: str, question: str) -> str:
    system = "You are a friendly HR screening assistant. Answer the recruiter's question about the candidate based on the provided candidate summary context."
    prompt = f"Candidate Context:\n{candidate_context}\n\nRecruiter's Question:\n{question}\n\nAnswer the question concisely."
    return ask_ai(prompt, system)
