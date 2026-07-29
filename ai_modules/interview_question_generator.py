from .core import ask_ai

def interview_question_generator(role: str, experience: int, skills: list, difficulty: str) -> str:
    system = """You are an expert technical interviewer. Generate relevant, high-quality interview questions based on the role, experience, focus skills, and difficulty.
You MUST provide a complete answer with exactly 2 questions under EACH of the following 4 subheaders without omitting any category:
#### Technical Questions
#### HR Questions
#### Coding Questions
#### Scenario Questions
Ensure every question is fully written out with explanation notes. Do not truncate any section."""
    prompt = f"Role: {role}\nExperience: {experience} years\nSkills to Focus: {skills}\nDifficulty: {difficulty}\n\nGenerate the complete set of questions for all 4 categories."
    return ask_ai(prompt, system, num_predict=2048)

