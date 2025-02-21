from typing import Dict
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

class ClaudeProcessor:
    def __init__(self, api_key: str):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def process(self, text: str) -> Dict:
        try:
            response = await self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": text}]
            )
            return {
                "model": "claude-3",
                "output": response.content[0].text,
                "tokens": response.usage.output_tokens
            }
        except Exception as e:
            raise Exception(f"Claude processing failed: {str(e)}") 