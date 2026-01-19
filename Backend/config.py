"""
Configuration settings for Campus Connect AI Engine
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", "8000"))
API_RELOAD: bool = os.getenv("API_RELOAD", "true").lower() == "true"

# Upload Configuration
UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB in bytes
ALLOWED_EXTENSIONS: list = [".pdf", ".docx", ".doc"]

# ATS Configuration
DEFAULT_MINIMUM_ATS_SCORE: float = float(os.getenv("DEFAULT_MINIMUM_ATS_SCORE", "50.0"))
SKILL_SIMILARITY_THRESHOLD: float = float(os.getenv("SKILL_SIMILARITY_THRESHOLD", "0.7"))

# Scoring Weights (can be adjusted)
SCORING_WEIGHTS: dict = {
    "skill": 0.40,
    "keyword": 0.25,
    "experience": 0.20,
    "education": 0.10,
    "format": 0.05
}

# Logging Configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# CORS Configuration (if needed in future)
CORS_ORIGINS: list = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# Application Metadata
APP_NAME: str = "Campus Connect AI Engine"
APP_VERSION: str = "1.0.0"
APP_DESCRIPTION: str = "AI-powered ATS (Applicant Tracking System) and Feedback Generator for Campus Connect"

# Database Configuration
POSTGRES_URL: str = os.getenv(
    "POSTGRES_URL",
    "postgresql://postgres:postgres@localhost:5432/campus_connect"
)
MONGODB_URL: str = os.getenv(
    "MONGODB_URL",
    "mongodb://localhost:27017/"
)
MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "campus_connect")

# JWT Configuration
JWT_SECRET_KEY: str = os.getenv(
    "JWT_SECRET_KEY",
    "your-secret-key-change-in-production-use-env-variable"
)
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))


