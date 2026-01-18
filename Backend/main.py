"""
FastAPI Main Application
Campus Connect AI Engine - Complete API with Database Integration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy import text
import os

from config import (
    APP_NAME, APP_VERSION, APP_DESCRIPTION,
    CORS_ORIGINS, UPLOAD_DIR
)
from database.postgres import engine, Base
from database.mongodb import mongo_client

# Import routers
from routers import auth, resume, ats, feedback, student, jobs, candidates

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(ats.router)
app.include_router(feedback.router)
app.include_router(student.router)
app.include_router(jobs.router)
app.include_router(candidates.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database connections on startup"""
    # Create uploads directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        print(f"Created {UPLOAD_DIR} directory")
    
    # Create database tables (in production, use Alembic migrations)
    # Base.metadata.create_all(bind=engine)
    
    print("="*60)
    print(f"{APP_NAME} - Starting Server")
    print("="*60)
    print("Database connections initialized")
    print("="*60)


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    mongo_client.close()
    print("Database connections closed")


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "endpoints": {
            "auth": "/api/v1/auth/*",
            "resume": "/api/v1/resume/*",
            "ats": "/api/v1/ats/*",
            "feedback": "/api/v1/feedback/*",
            "student": "/api/v1/student/*",
            "jobs": "/api/v1/jobs/*",
            "candidates": "/api/v1/candidates/*",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check PostgreSQL connection
        from database.postgres import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        postgres_status = "connected"
    except Exception as e:
        postgres_status = f"error: {str(e)}"
    
    try:
        # Check MongoDB connection
        from database.mongodb import get_mongo_db
        mongo_db = get_mongo_db()
        mongo_db.command("ping")
        mongodb_status = "connected"
    except Exception as e:
        mongodb_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if postgres_status == "connected" and mongodb_status == "connected" else "degraded",
        "timestamp": datetime.now().isoformat(),
        "service": APP_NAME,
        "databases": {
            "postgresql": postgres_status,
            "mongodb": mongodb_status
        }
    }


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )
