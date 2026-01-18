"""ATS engine router"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from database.postgres import get_db
from database.mongodb import get_mongo_db
from database.models import User, Job, Application, Evaluation
from database.schemas import ATSScoreRequest, ATSScoreResponse, EvaluationResponse
from models import JobRequirement, ResumeData
from ats_engine import ATSEngine
from resume_parser import ResumeParser
from auth.dependencies import get_current_active_user

router = APIRouter(prefix="/api/v1/ats", tags=["ATS"])

# Initialize engines
ats_engine = ATSEngine()
resume_parser = ResumeParser()


@router.post("/score", response_model=ATSScoreResponse)
async def score_resume(
    request: ATSScoreRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Score resume against job requirements"""
    try:
        # Get resume data
        resume_data = None
        if request.resume_id:
            mongo_db = get_mongo_db()
            resume_doc = mongo_db.resumes.find_one({"resume_id": request.resume_id})
            if not resume_doc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Resume not found"
                )
            parsed_data = resume_doc.get("parsed_data", {})
            resume_data = ResumeData(**parsed_data)
        elif request.resume_text:
            parsed_data = resume_parser.parse(resume_text=request.resume_text)
            resume_data = ResumeData(**parsed_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either resume_id or resume_text must be provided"
            )
        
        # Parse job requirement
        job_requirement = JobRequirement(**request.job_requirement)
        
        # Score resume
        ats_result = ats_engine.score_resume(resume_data, job_requirement)
        
        # Store detailed result in MongoDB
        mongo_db = get_mongo_db()
        result_id = str(uuid.uuid4())
        result_doc = {
            "result_id": result_id,
            "user_id": current_user.id,
            "ats_result": ats_result,
            "resume_data": resume_data.dict(),
            "job_requirement": job_requirement.dict()
        }
        mongo_db.ats_results.insert_one(result_doc)
        
        return ATSScoreResponse(
            evaluation_id=0,  # Will be set if linked to application
            ats_score=ats_result["ats_score"],
            passed=ats_result["passed"],
            skill_match_score=ats_result["skill_match_score"],
            education_score=ats_result["education_score"],
            experience_score=ats_result["experience_score"],
            keyword_match_score=ats_result["keyword_match_score"],
            format_score=ats_result["format_score"],
            matched_skills=ats_result["matched_skills"],
            missing_skills=ats_result["missing_skills"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error scoring resume: {str(e)}"
        )


@router.get("/evaluation/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation(
    evaluation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get evaluation details"""
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found"
        )
    
    # Check access (user must be related to the application or be admin)
    application = evaluation.application
    if (application.candidate.user_id != current_user.id and 
        application.job.created_by != current_user.id and 
        current_user.role.value != "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this evaluation"
        )
    
    return evaluation


@router.post("/batch-score")
async def batch_score(
    requests: List[ATSScoreRequest],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Score multiple resumes"""
    results = []
    for request in requests:
        try:
            result = await score_resume(request, current_user, db)
            results.append(result.dict())
        except Exception as e:
            results.append({"error": str(e)})
    
    return {"results": results, "total": len(results)}
