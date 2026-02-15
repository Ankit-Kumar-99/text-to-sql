import os
import time
from dotenv import load_dotenv
from google import genai
from app.config import MODEL_NAME, GEN_CONFIG

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY missing in .env")

client = genai.Client(api_key=API_KEY)


def call_gemini(prompt: str, retries: int = 2) -> str:
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=GEN_CONFIG
            )
            return response.text.strip()

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1.5)
            else:
                raise e
