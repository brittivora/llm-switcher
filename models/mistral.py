import os
import time
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path

# Load environment
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_mistral(prompt: str):
    model_id = "mistral-saba-24b"
    return call_model(prompt, model_id)

def call_model(prompt: str, model_id: str):
    start = time.time()
    
    try:
        stream = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=512,
            top_p=1,
            stream=True,
        )

        output = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                output += delta

        latency = round((time.time() - start) * 1000, 2)
        token_count = len(prompt.split()) + len(output.split())

        return output.strip(), token_count, latency

    except Exception as e:
        print("Error calling Mistral model:", str(e))
        raise RuntimeError("Mistral (Groq) call failed")
