import ollama

MODEL = "gemma3:4b"

def ask_ai(prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        response = ollama.chat(
            model=MODEL, 
            messages=messages,
            options={
                "temperature": 0.3,
                "num_predict": 450,  # Limits output length to guarantee generation under 30 seconds
                "top_k": 40,
                "top_p": 0.9
            }
        )
        return response["message"]["content"]
    except Exception as e:
        return f"AI service unavailable: {e}"
