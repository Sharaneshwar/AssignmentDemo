from fastapi import FastAPI
from pydantic import BaseModel
from ctransformers import AutoModelForCausalLM

app = FastAPI()

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    "models/llama-2-7b-chat.Q4_K_M.gguf",
    model_type="llama",
    gpu_layers=0
)
print("Model loaded!")

class Prompt(BaseModel):
    text: str

@app.post("/ask")
def generate_text(prompt: Prompt):
    output = model(prompt.text, max_new_tokens=100)
    return {"response": output}

@app.get("/")
async def root():
    return {"message": "Welcome to the Models API!"}