from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

UPLOAD_FOLDER: str = str(BASE_DIR / "uploads")

CHROMA_DB_PATH: str = str(BASE_DIR / "chroma_db")

WHISPER_MODEL: str = "base"

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")