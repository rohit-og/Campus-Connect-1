"""Resume parser router"""

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
from database.postgres import get_db
from database.mongodb import get_mongo_db
from database.schemas import ResumeParseRequest, ResumeParseResponse
from resume_parser import ResumeParser
from auth.dependencies import get_current_active_user
from database.models import User
from config import UPLOAD_DIR, ALLOWED_EXTENSIONS

router = APIRouter(prefix="/api/v1/resume", tags=["Resume"])

# Initialize parser
resume_parser = ResumeParser()

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/parse", response_model=ResumeParseResponse)
async def parse_resume(
    request: ResumeParseRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Parse resume from text"""
    if not request.resume_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="resume_text is required"
        )
    
    try:
        # Parse resume
        parsed_data = resume_parser.parse(resume_text=request.resume_text)
        
        # Store in MongoDB
        mongo_db = get_mongo_db()
        resume_id = str(uuid.uuid4())
        
        resume_doc = {
            "resume_id": resume_id,
            "user_id": current_user.id,
            "raw_text": parsed_data.get("raw_text", ""),
            "parsed_data": parsed_data,
            "created_at": str(uuid.uuid4())  # Use timestamp in production
        }
        
        mongo_db.resumes.insert_one(resume_doc)
        
        return ResumeParseResponse(
            resume_id=resume_id,
            parsed_data=parsed_data,
            message="Resume parsed successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing resume: {str(e)}"
        )


@router.post("/upload", response_model=ResumeParseResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload and parse resume file"""
    # Validate file extension
    file_extension = os.path.splitext(file.filename)[1].lower() if file.filename else ""
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Save file temporarily
    resume_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{resume_id}{file_extension}")
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse resume
        parsed_data = resume_parser.parse(file_path=file_path)
        
        # Store in MongoDB
        mongo_db = get_mongo_db()
        resume_doc = {
            "resume_id": resume_id,
            "user_id": current_user.id,
            "filename": file.filename,
            "raw_text": parsed_data.get("raw_text", ""),
            "parsed_data": parsed_data,
            "created_at": str(uuid.uuid4())  # Use timestamp in production
        }
        
        mongo_db.resumes.insert_one(resume_doc)
        
        return ResumeParseResponse(
            resume_id=resume_id,
            parsed_data=parsed_data,
            message="Resume uploaded and parsed successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


@router.get("/{resume_id}", response_model=ResumeParseResponse)
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get parsed resume data"""
    mongo_db = get_mongo_db()
    resume_doc = mongo_db.resumes.find_one({"resume_id": resume_id})
    
    if not resume_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Check if user has access (owner or admin)
    if resume_doc.get("user_id") != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resume"
        )
    
    return ResumeParseResponse(
        resume_id=resume_id,
        parsed_data=resume_doc.get("parsed_data", {}),
        message="Resume retrieved successfully"
    )
