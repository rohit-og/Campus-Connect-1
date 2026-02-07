"""
Database configuration for Campus Connect
Provides SQLAlchemy setup for aptitude module and other features
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - can be overridden with environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./campus_connect.db")

# Create engine
# For SQLite, we need check_same_thread=False
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False  # Set to True for SQL query logging
    )
else:
    engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """
    Database dependency for FastAPI
    Yields a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
