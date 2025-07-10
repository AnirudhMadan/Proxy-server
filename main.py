from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = "gemini-1.5-pro-latest"

class PromptRequest(BaseModel):
    prompt: str
    instructions: str = ""

@app.post("/gemini")
async def query_gemini(request: PromptRequest):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}

    full_prompt = f"{request.instructions}\n\n{request.prompt}" if request.instructions else request.prompt

    payload = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            output = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            return {"result": output}
        else:
            return {"error": res.status_code, "details": res.json()}
    except Exception as e:
        return {"error": "Exception", "message": str(e)}
