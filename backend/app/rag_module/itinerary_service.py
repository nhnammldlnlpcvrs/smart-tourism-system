# backend/app/rag_module/itinerary_service.py
from app.api.llm_module import ask_gemini

def generate_itinerary(prompt):
    return ask_gemini(prompt)