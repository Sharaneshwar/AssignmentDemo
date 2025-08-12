import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=GROQ_API_KEY)

class GenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = "groq"
    max_tokens: Optional[int] = 4096

def generate_with_groq(prompt: str, max_tokens: int) -> str:
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_completion_tokens=max_tokens,
        top_p=0.95,
        stream=False,
        stop=None
    )
    return completion.choices[0].message.content

@app.post("/generate")
async def generate_text(request: GenerateRequest):
    if request.model == "groq":
        result = generate_with_groq(request.prompt, request.max_tokens)
        return {"model": "groq", "response": result}
    elif request.model:
        raise HTTPException(status_code=501, detail=f"Model '{request.model}' not implemented yet.")
    else:
        raise HTTPException(status_code=400, detail="Model must be specified.")
