import subprocess

OLLAMA_MODEL = "llama3"

SYSTEM_STYLE_PROMPT = """
You are a helpful AI assistant.

- Answer clearly and concisely
- Use simple language
- Be structured when needed
"""


def call_ollama(prompt: str) -> str:
    full_prompt = f"{SYSTEM_STYLE_PROMPT}\n\nUser: {prompt}\nAssistant:"

    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=60
        )

        return result.stdout.strip()

    except Exception as e:
        return f"Ollama error: {e}"


def ask_llm(question: str) -> str:
    """
    Main function for generic question answering
    """
    return call_ollama(question)