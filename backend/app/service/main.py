'''
from llm_agent import LLMAgent

if __name__ == "__main__":
    agent = LLMAgent()

    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        reply = agent.handle_query(user_input)
        print("🤖 LLM:", reply)


from fastapi import FastAPI
from pydantic import BaseModel
from llm_agent import LLMAgent

app = FastAPI(title="Weather + LLM API", description="API kết hợp Open-Meteo và ChatGPT", version="1.0")

agent = LLMAgent()

class QueryRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Welcome to Weather LLM API"}

@app.post("/ask")
def ask_weather(req: QueryRequest):
    """API chính để hỏi LLM"""
    reply = agent.handle_query(req.message)
    return {"reply": reply}
'''


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from pydantic import BaseModel
from services.llm_agent import LLMAgent  # <- import tương đối

app = FastAPI(
    title="Weather + LLM API",
    description="API kết hợp Open-Meteo và ChatGPT",
    version="1.0"
)

agent = LLMAgent()

class QueryRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Welcome to Weather LLM API"}

@app.post("/ask")
def ask_weather(req: QueryRequest):
    """Gửi câu hỏi đến LLM hoặc lấy thời tiết"""
    reply = agent.handle_query(req.message)
    return {"reply": reply}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

