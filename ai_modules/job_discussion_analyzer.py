from .core import ask_ai

def job_discussion_analyzer(transcript: str) -> str:
    system = """You are a senior interviewer analyzer. Analyze the interview transcript or conversation notes thoroughly. 
You MUST provide a complete answer structured under exactly these 4 subheaders without cutting off:
#### Communication Assessment
#### Technical Confidence
#### Positive & Negative Points
#### Final Recommendation
Ensure every section contains a clear, concise, and fully completed evaluation."""
    prompt = f"Interview Transcript/Notes:\n{transcript}\n\nProvide the complete 4-section evaluation."
    return ask_ai(prompt, system, num_predict=2048)

