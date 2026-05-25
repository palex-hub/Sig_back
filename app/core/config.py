import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/sig")
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
