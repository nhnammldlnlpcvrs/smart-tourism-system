from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger
from .utils import chatbot_reply  # Import từ utils.py trong cùng thư mục

app = FastAPI(title="Smart Tourism Chatbot API")
security = HTTPBasic()

@app.get("/")
def root():
    return {"message": "Welcome to Smart Tourism Chatbot API!"}

@app.get("/metadata")
def get_metadata():
    return {"project": "Smart Tourism Chatbot", "version": "1.0", "author": "Nam Nguyen"}

@app.post("/chat")
def chat(question: str):
    """
    Chat API chính: trả lời từ dữ liệu landmarks.json trước, nếu thiếu gọi GPT hỗ trợ.
    """
    logger.info(f"[USER] {question}")
    try:
        answer = chatbot_reply(question)
        logger.info(f"[BOT] {answer}")
        return {"response": answer}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/chat-auth")
def chat_auth(
    question: str,
    credentials: HTTPBasicCredentials = Depends(security)
):
    """
    Chat có xác thực chỉ dành cho Admin (nếu cần test bảo mật)
    """
    if credentials.username != "admin" or credentials.password != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    logger.info(f"[AUTH USER] {credentials.username} asked: {question}")
    answer = chatbot_reply(question)
    return {"response": answer}