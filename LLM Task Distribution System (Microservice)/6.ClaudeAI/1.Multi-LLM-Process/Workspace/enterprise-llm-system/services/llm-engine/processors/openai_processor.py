from typing import Dict
import openai
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

class OpenAIProcessor:
    def __init__(self, api_key: str):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def process(self, text: str) -> Dict:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": text}],
                temperature=0.7
            )
            return {
                "model": "gpt-4",
                "output": response.choices[0].message.content,
                "tokens": response.usage.total_tokens
            }
        except Exception as e:
            raise Exception(f"OpenAI processing failed: {str(e)}") 