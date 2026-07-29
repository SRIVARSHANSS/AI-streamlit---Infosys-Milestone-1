from .core import ask_ai

def resume_chat(candidate_context: str, question: str) -> str:
    system = "You are a friendly HR screening assistant. Answer the recruiter's question about the candidate based on the provided candidate summary context thoroughly and completely."
    prompt = f"Candidate Context:\n{candidate_context}\n\nRecruiter's Question:\n{question}\n\nProvide a full, complete, and accurate answer."
    return ask_ai(prompt, system, num_predict=2048)

