"""
Configuration settings for Campus Connect AI Engine
"""

import os
from typing import Optional

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


