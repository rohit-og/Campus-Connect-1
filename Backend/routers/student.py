"""Student engine router"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database.postgres import get_db
from database.models import User, Job
from database.schemas import (
    JobSearchRequest, JobSearchResponse,
    SkillGapRequest, SkillGapResponse,
    ResumeFeedbackRequest,
    RejectionInterpretRequest, RejectionInterpretResponse
)
from student_engine import CampusConnectStudentEngine
from auth.dependencies import get_current_active_user

router = APIRouter(prefix="/api/v1/student", tags=["Student"])

# Initialize student engine
student_engine = CampusConnectStudentEngine()


@router.post("/jobs/search", response_model=List[JobSearchResponse])
async def search_jobs(
    request: JobSearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Natural language job search"""
    try:
        # Get all jobs from database
        jobs = db.query(Job).all()
        
        # Convert to list of dicts for student engine
        jobs_list = []
        for job in jobs:
            requirements = job.requirements_json or {}
            jobs_list.append({
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "salary": job.salary,
                "description": job.description or "",
                "requirements": requirements.get("job_description", "") or 
                              f"{', '.join(requirements.get('required_skills', []))}"
            })
        
        # Search jobs using student engine
        results = student_engine.search_jobs(
            student_query=request.query,
            jobs=jobs_list,
            student_skills=request.student_skills,
            top_k=request.top_k
        )
        
        # Convert to response format
        response_list = []
        for result in results:
            response_list.append(JobSearchResponse(
                job_id=result.get("job_id", 0),
                title=result.get("title", ""),
                company=result.get("company", ""),
                location=result.get("location"),
                salary=result.get("salary"),
                match_score=result.get("match_score", 0.0),
                application_status=result.get("application_status", "Recommended"),
                missing_skills=result.get("missing_skills", []),
                matched_skills=result.get("matched_skills", []),
                message=result.get("message", ""),
                required_skills=result.get("required_skills", [])
            ))
        
        return response_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching jobs: {str(e)}"
        )


@router.post("/skill-gap/analyze", response_model=SkillGapResponse)
async def analyze_skill_gap(
    request: SkillGapRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Analyze skill gap between student and job requirements"""
    try:
        result = student_engine.analyze_skill_gap(
            student_skills=request.student_skills,
            job_skills=request.job_skills,
            job_role=request.job_role
        )
        
        return SkillGapResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing skill gap: {str(e)}"
        )


@router.post("/resume/feedback")
async def get_resume_feedback(
    request: ResumeFeedbackRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get resume feedback for ATS optimization"""
    try:
        result = student_engine.get_resume_feedback(
            resume_text=request.resume_text,
            job_description=request.job_description,
            job_requirements=request.job_requirements,
            skill_gap_output=request.skill_gap_output
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating resume feedback: {str(e)}"
        )


@router.post("/rejection/interpret", response_model=RejectionInterpretResponse)
async def interpret_rejection(
    request: RejectionInterpretRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Interpret rejection feedback"""
    try:
        result = student_engine.interpret_rejection(
            rejection_feedback=request.rejection_feedback,
            job_title=request.job_title,
            student_skills=request.student_skills
        )
        
        return RejectionInterpretResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interpreting rejection: {str(e)}"
        )
