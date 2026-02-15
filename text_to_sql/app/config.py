import os

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

GEN_CONFIG = {
    "temperature": 0.2,
    "max_output_tokens": 512
}

ALLOWED_TABLE = "marketing_lens.ga4_events"
