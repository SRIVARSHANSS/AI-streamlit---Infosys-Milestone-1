from .core import ask_ai

def job_discussion_analyzer(transcript: str) -> str:
    system = """You are a senior interviewer analyzer. Analyze the interview transcript or conversation notes. 
You must always structure your output under exactly these 4 subheaders:
#### Communication Assessment
#### Technical Confidence
#### Positive & Negative Points
#### Final Recommendation"""
    prompt = f"Interview Transcript/Notes:\n{transcript}\n\nProvide the 4-section structured evaluation."
    return ask_ai(prompt, system)
