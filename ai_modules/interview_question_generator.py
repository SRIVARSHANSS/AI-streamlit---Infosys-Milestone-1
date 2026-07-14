from .core import ask_ai

def interview_question_generator(role: str, experience: int, skills: list, difficulty: str) -> str:
    system = """You are an expert technical interviewer. Generate relevant interview questions based on the role, experience, focus skills, and difficulty.
You must always structure your output under exactly these 4 subheaders:
#### Technical Questions
#### HR Questions
#### Coding Questions
#### Scenario Questions"""
    prompt = f"Role: {role}\nExperience: {experience} years\nSkills to Focus: {skills}\nDifficulty: {difficulty}\n\nGenerate the questions."
    return ask_ai(prompt, system)
