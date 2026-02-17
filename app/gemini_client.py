import google.generativeai as genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)


def generate_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()
