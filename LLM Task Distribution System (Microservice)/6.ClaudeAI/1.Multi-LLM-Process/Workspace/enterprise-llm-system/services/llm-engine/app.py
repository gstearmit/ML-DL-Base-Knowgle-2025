from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from typing import List
import aiohttp

app = FastAPI()

class LLMRequest(BaseModel):
    task_id: str
    input_text: str
    models: List[str]

@app.post("/api/llm/process")
async def process_llm(request: LLMRequest):
    try:
        tasks = []
        for model in request.models:
            if model == "gpt-4":
                tasks.append(process_openai(request.input_text))
            elif model == "claude":
                tasks.append(process_anthropic(request.input_text))
            elif model == "gemini":
                tasks.append(process_google(request.input_text))
                
        results = await asyncio.gather(*tasks)
        return {"task_id": request.task_id, "results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 