from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


class Settings:
    BASE_DIR = BASE_DIR
    API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    KNOWLEDGE_DIR = BASE_DIR / "data" / "manuales"


settings = Settings()
