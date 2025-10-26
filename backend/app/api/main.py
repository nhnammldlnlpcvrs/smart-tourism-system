from fastapi import FastAPI
from pydantic import BaseModel
from app.api.llm_module import ask_gemini

app = FastAPI(title="Smart Tourism Chatbot")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Smart Tourism Backend is running!"}

@app.post("/chat")
def chat(request: ChatRequest):
    reply = ask_gemini(request.message)
    return {"user_message": request.message, "bot_reply": reply}