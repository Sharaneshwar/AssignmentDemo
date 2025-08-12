import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class ModelRequest(BaseModel):
    prompt: str
    model: Optional[str] = "openai"
    max_tokens: Optional[int] = 1024

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise RuntimeError("HUGGINGFACE_API_KEY environment variable is not set")

client = InferenceClient(
    provider="cerebras",
    api_key=HUGGINGFACE_API_KEY,
)

MODEL_MAP = {
    "openai": "openai/gpt-oss-120b",
    "deepseek": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
}

def ask_model(prompt: str, max_tokens: int, model) -> str:
    result = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=max_tokens,
        stream=False,
        temperature=0.6
    )
    return result.choices[0].message.content

@app.post("/ask")
async def generate_text(request: ModelRequest):
    if request.model in MODEL_MAP:
        model = MODEL_MAP[request.model]
        response = ask_model(request.prompt, request.max_tokens, model)
        return {"response": response}
    elif request.model:
        raise HTTPException(status_code=501, detail=f"Model '{request.model}' not implemented yet.")
    else:
        raise HTTPException(status_code=400, detail="Model must be specified.")

@app.get("/")
async def root():
    return {"message": "Welcome to the Models API!"}