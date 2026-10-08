from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


class Settings:
    BASE_DIR = BASE_DIR
    API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    FALLBACK_MODELS = [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
    ]
    KNOWLEDGE_DIR = BASE_DIR / "data" / "manuales"
    VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"

settings = Settings()
