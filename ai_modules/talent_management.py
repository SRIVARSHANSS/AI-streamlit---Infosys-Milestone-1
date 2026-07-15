from .core import ask_ai

def talent_management_summary(name: str, role: str, department: str, tenure: str, performance_history: list) -> str:
    history_text = "\n".join(
        f"- {entry['date']}: {entry['rating']}" for entry in performance_history
    )
    system = (
        "You are an HR Talent Management Advisor with expertise in performance evaluation "
        "and promotion planning. You write structured, evidence-based assessments, not vague praise."
    )
    prompt = (
        f"Employee: {name}\nCurrent Role: {role}\nDepartment: {department}\nTenure: {tenure}\n\n"
        f"Performance history (oldest to newest):\n{history_text}\n\n"
        "Respond under exactly these four headers:\n"
        "#### Performance Trend\n"
        "#### Key Strengths\n"
        "#### Areas for Development\n"
        "#### Promotion Readiness\n"
        "For Promotion Readiness, give one clear verdict: 'Ready Now', 'Ready in 6-12 Months', "
        "or 'Not Yet Ready', followed by 2-3 sentences of reasoning based specifically on the "
        "performance trend shown above."
    )
    return ask_ai(prompt, system)
