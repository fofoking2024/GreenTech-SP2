import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Prefer DATABASE_URL env var, else use SQLite file in project root
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///greentech.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "SP2@2026")
