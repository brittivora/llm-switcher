from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .models_utils import route_model
import csv, os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "prompts_log.csv")
os.makedirs(LOG_DIR, exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["timestamp", "model", "prompt", "response", "token_count", "latency_ms"])

@app.post("/generate")
def generate(request: PromptRequest, model: str = Query(..., enum=["llama2", "mistral"])):
    print(f"📥 Prompt received: {request.prompt}, model: {model}")
    try:
        response, tokens, latency = route_model(model, request.prompt)

        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow([
                datetime.now().isoformat(),
                model,
                request.prompt.replace("\n", " "),
                response.replace("\n", " "),
                tokens,
                latency
            ])
        print("✅ Logged to:", os.path.abspath(LOG_FILE))

        return {
            "model": model,
            "prompt": request.prompt,
            "response": response,
            "token_count": tokens,
            "latency_ms": latency
        }

    except Exception as e:
        print("❌ Exception:", e)
        return {"error": str(e)}
