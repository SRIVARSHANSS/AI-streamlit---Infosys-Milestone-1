from .core import ask_ai

def chatbot_query(user_query: str, candidates_context: str) -> str:
    system = "You are a helpful recruitment chatbot. You have access to a summary table of candidates. Answer the user's questions or queries regarding the candidate pool using the table."
    prompt = f"Candidates Summary Table:\n{candidates_context}\n\nUser Query: {user_query}\n\nRespond with an appropriate answer."
    return ask_ai(prompt, system)
