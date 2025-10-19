from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loguru import logger
from .utils import chatbot_reply

app = FastAPI(title="Smart Tourism Chatbot API", version="1.0")

# Request body schema
class ChatRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Smart Tourism Chatbot is running!"}

@app.get("/metadata")
def get_metadata():
    return {"project": "Smart Tourism Chatbot", "version": "1.0", "author": "top7vibecoder"}

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Chat API: nhận question từ body JSON
    Ví dụ: POST /chat
    {
        "question": "Hội An có gì đẹp?"
    }
    """
    try:
        logger.info(f"User hỏi: {request.question}")
        answer = chatbot_reply(request.question)
        return {"answer": answer}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Lỗi server nội bộ")