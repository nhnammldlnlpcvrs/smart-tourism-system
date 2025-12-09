# backend/app/rag_module/generator.py
from typing import Optional
import asyncio

# we assume your existing LLM wrapper is at app.api.llm_module.ask_gemini
# It might be async; this wrapper calls it safely.
try:
    from app.api.llm_module import ask_gemini
except Exception:
    async def ask_gemini(prompt: str, **kwargs):
        # fallback: echo prompt if LLM not configured
        return "LLM not configured. Prompt head:\n" + prompt[:1600]

class LLMGenerator:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name

    def generate(self, prompt: str, timeout: int = 60):
        try:
            coro = ask_gemini(prompt)
            if asyncio.iscoroutine(coro):
                return asyncio.run(coro)
            return coro
        except Exception as e:
            return f"LLM error: {e}"