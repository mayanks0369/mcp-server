from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

X_API_KEY = os.getenv("X_API_KEY", "default-fallback-key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
