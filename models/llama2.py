import os
import time
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env from parent directory
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in .env")

def call_llama2(prompt: str):
    model = "llama3-8b-8192"
    return call_model(prompt, model)

def call_model(prompt: str, model_id: str):
    start = time.time()

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200,
        "stop": None  # Optional: Avoids stopping early
    }

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        res.raise_for_status()

        output = res.json()["choices"][0]["message"]["content"]
        latency = round((time.time() - start) * 1000, 2)
        token_count = len(prompt.split()) + len(output.split())

        return output.strip(), token_count, latency

    except Exception as e:
        print("Error calling Groq model:", str(e))
        print("Full Response:", res.text)
        raise RuntimeError("Groq model failed to generate output.")
