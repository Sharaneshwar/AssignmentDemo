# LLM API with Quantized and Cloud Models

## Overview

This project provides a FastAPI backend using REST that integrates multiple large language models (LLMs) to perform natural language tasks such as resume parsing. It supports both heavy cloud-hosted models for complex tasks and lightweight local models for efficient inference.

You can send POST requests to our deployed API at:

`https://llmapi-p5i9.onrender.com/ask`


## Model Exploration and Choices

### Heavy LLMs (DeepSeek & OpenAI GPT)

- **Models Used:**  
  - DeepSeek-R1 series
  - OpenAI GPT models accessed via Hugging Face hosted APIs

- **Why Chosen:**  
  - These models provide excellent language understanding and generation capabilities, suitable for complex tasks including resume parsing and reasoning.  
  - Using hosted APIs avoids the need for expensive infrastructure and simplifies deployment.

- **Trade-offs:**  
  - Higher latency and cost per request due to large model sizes and compute demands.  
  - Not ideal for simple or low-latency tasks.

---

### Lightweight 4-bit Quantized Models

- **Model Used:**  
  - `TheBloke/Llama-2-7B-Chat-Q4_K_M.gguf` — a 4-bit quantized Llama 2 7B Chat model.

- **Why Chosen:**  
  - Lightweight and optimized for local inference with low memory and CPU/GPU usage.  
  - Suitable for fast, simple NLP tasks like basic resume parsing or prototyping.

- **Current Status:**  
  - Model downloaded and tested locally (localmodel.py).
  - Not yet self-hosted due to lack of free-tier cloud resources and expiration of free tier in AWS.


## Architecture

- FastAPI exposes a `/ask` POST endpoint accepting prompts, model selection and max tokens.  
- Supports two backend flows:
  - **DeepSeek / OpenAI GPT** via Hugging Face API for heavy LLM inference.  
  - **Quantized Llama 2** model locally (planned for self-hosting).

## Installation

### Prerequisites

- Python 3.10+  
- Git (optional)

### Create and Activate Virtual Environment

```bash
python -m venv myenv
myenv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project containing your Hugging Face API key:

```plaintext    
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

### Run the API Server

```bash
uvicorn app:app --reload
```

### Test the API
You can test the API using Powershell or any HTTP client:

```bash
Invoke-RestMethod -Uri "http://localhost:8000/ask" `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{ "prompt": "What is the capital of India?", "model": "openai", "max_tokens": 100 }'
```

## API Documentation
The API documentation is available at `/docs` route for interactive testing and exploration of endpoints.
