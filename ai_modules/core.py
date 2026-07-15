import ollama

MODEL = "gemma3:4b"

def ask_ai(prompt: str, system: str = "") -> str:
    messages = []
    # Check if the system prompt is requesting a structured JSON format
    is_json_request = system and ("json" in system.lower() or "{" in system)
    
    if is_json_request:
        full_system = system
    else:
        # Globally instruct the model to produce detailed, exhaustive analyses rather than short summaries
        detailed_instruction = (
            " Always write a highly detailed, comprehensive, and exhaustive response. "
            "Provide thorough breakdowns and deep reasoning. Avoid brief or single-sentence answers."
        )
        full_system = (system + detailed_instruction) if system else ("You are a helpful recruitment assistant." + detailed_instruction)
    
    messages.append({"role": "system", "content": full_system})
    messages.append({"role": "user", "content": prompt})
    try:
        response = ollama.chat(
            model=MODEL, 
            messages=messages,
            options={
                "temperature": 0.3,
                "num_predict": 900,  # Limits output length to keep generation under 1 minute
                "top_k": 40,
                "top_p": 0.9
            }
        )
        return response["message"]["content"]
    except Exception as e:
        return f"AI service unavailable: {e}"
