"""
FastAPI Main Application
Campus Connect AI Engine - ATS and Feedback System
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
import os
import uuid
import json
from datetime import datetime

from models import (
    JobRequirement, ResumeData, ATSResult, RejectionFeedback,
    CandidateEvaluationRequest, CandidateEvaluationResponse
)
from resume_parser import ResumeParser
from ats_engine import ATSEngine
from feedback_generator import FeedbackGenerator

# Initialize FastAPI app
app = FastAPI(
    title="Campus Connect AI Engine",
    description="AI-powered ATS (Applicant Tracking System) and Feedback Generator for Campus Connect",
    version="1.0.0"
)

# Initialize components
resume_parser = ResumeParser()
ats_engine = ATSEngine()
feedback_generator = FeedbackGenerator()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Campus Connect AI Engine - ATS and Feedback System",
        "version": "1.0.0",
        "endpoints": {
            "evaluate_candidate": "/api/v1/evaluate",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Campus Connect AI Engine"
    }


@app.post("/api/v1/evaluate", response_model=CandidateEvaluationResponse)
async def evaluate_candidate(
    job_requirement: str = Form(..., description="JSON string of JobRequirement"),
    resume_file: Optional[UploadFile] = File(None, description="Resume file (PDF or DOCX)"),
    resume_text: Optional[str] = Form(None, description="Resume text content (alternative to file)")
):
    """
    Main endpoint for evaluating a candidate against job requirements
    
    This endpoint:
    1. Parses the resume (from file or text)
    2. Scores the candidate using ATS
    3. Returns feedback if candidate is rejected
    
    Args:
        job_requirement: JSON string containing job requirements
        resume_file: Optional resume file (PDF or DOCX)
        resume_text: Optional resume text content
        
    Returns:
        CandidateEvaluationResponse with ATS score and feedback (if rejected)
    """
    try:
        # Parse job requirement
        try:
            job_req_dict = json.loads(job_requirement)
            job_req = JobRequirement(**job_req_dict)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON in job_requirement: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid job requirement format: {str(e)}")
        
        # Validate that either file or text is provided
        if not resume_file and not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Either resume_file or resume_text must be provided"
            )
        
        # Generate unique candidate ID
        candidate_id = str(uuid.uuid4())
        
        # Parse resume
        resume_file_path = None
        try:
            if resume_file:
                # Save uploaded file
                file_extension = os.path.splitext(resume_file.filename)[1] if resume_file.filename else ".pdf"
                resume_file_path = os.path.join(UPLOAD_DIR, f"{candidate_id}{file_extension}")
                
                with open(resume_file_path, "wb") as f:
                    content = await resume_file.read()
                    f.write(content)
                
                parsed_resume = resume_parser.parse(file_path=resume_file_path)
            else:
                parsed_resume = resume_parser.parse(resume_text=resume_text)
            
            # Convert to ResumeData model
            resume_data = ResumeData(**parsed_resume)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing resume: {str(e)}")
        finally:
            # Clean up uploaded file
            if resume_file_path and os.path.exists(resume_file_path):
                try:
                    os.remove(resume_file_path)
                except:
                    pass
        
        # Score resume using ATS
        try:
            ats_result_dict = ats_engine.score_resume(resume_data, job_req)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error scoring resume: {str(e)}")
        
        # Create ATSResult
        ats_result = ATSResult(
            candidate_id=candidate_id,
            ats_score=ats_result_dict['ats_score'],
            passed=ats_result_dict['passed'],
            skill_match_score=ats_result_dict['skill_match_score'],
            education_score=ats_result_dict['education_score'],
            experience_score=ats_result_dict['experience_score'],
            keyword_match_score=ats_result_dict['keyword_match_score'],
            format_score=ats_result_dict['format_score'],
            matched_skills=ats_result_dict['matched_skills'],
            missing_skills=ats_result_dict['missing_skills'],
            recommendations=[]  # Will be filled by feedback if rejected
        )
        
        # Generate feedback if rejected
        feedback = None
        message = ""
        
        if not ats_result.passed:
            try:
                feedback_dict = feedback_generator.generate_feedback(
                    ats_result_dict, parsed_resume, job_req
                )
                
                if feedback_dict:
                    feedback = RejectionFeedback(
                        candidate_id=candidate_id,
                        ats_score=ats_result.ats_score,
                        minimum_required_score=job_req.minimum_ats_score,
                        rejection_reasons=feedback_dict['rejection_reasons'],
                        missing_critical_skills=feedback_dict['missing_critical_skills'],
                        resume_strengths=feedback_dict['resume_strengths'],
                        resume_weaknesses=feedback_dict['resume_weaknesses'],
                        improvement_recommendations=feedback_dict['improvement_recommendations'],
                        format_issues=feedback_dict['format_issues'],
                        mistake_highlights=feedback_dict['mistake_highlights']
                    )
                    
                    message = (
                        f"Candidate rejected. ATS Score: {ats_result.ats_score:.2f}% "
                        f"(Minimum Required: {job_req.minimum_ats_score}%). "
                        f"Feedback provided with {len(feedback.rejection_reasons)} rejection reasons and "
                        f"{len(feedback.improvement_recommendations)} recommendations."
                    )
            except Exception as e:
                # If feedback generation fails, still return ATS result
                message = f"Candidate rejected. Error generating detailed feedback: {str(e)}"
        else:
            message = (
                f"Candidate PASSED! ATS Score: {ats_result.ats_score:.2f}% "
                f"(Minimum Required: {job_req.minimum_ats_score}%). "
                f"Matched {len(ats_result.matched_skills)} skills."
            )
        
        # Build response
        response = CandidateEvaluationResponse(
            candidate_id=candidate_id,
            ats_result=ats_result,
            feedback=feedback,
            message=message
        )
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/v1/evaluate-json")
async def evaluate_candidate_json(request: CandidateEvaluationRequest):
    """
    Alternative endpoint that accepts JSON body instead of form data
    
    Use this endpoint if you prefer sending JSON instead of form-data
    """
    try:
        job_req = request.job_requirement
        
        # Validate that either file or text is provided
        if not request.resume_file_path and not request.resume_text:
            raise HTTPException(
                status_code=400,
                detail="Either resume_file_path or resume_text must be provided"
            )
        
        # Generate unique candidate ID
        candidate_id = str(uuid.uuid4())
        
        # Parse resume
        try:
            if request.resume_file_path:
                parsed_resume = resume_parser.parse(file_path=request.resume_file_path)
            else:
                parsed_resume = resume_parser.parse(resume_text=request.resume_text)
            
            resume_data = ResumeData(**parsed_resume)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing resume: {str(e)}")
        
        # Score resume using ATS
        try:
            ats_result_dict = ats_engine.score_resume(resume_data, job_req)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error scoring resume: {str(e)}")
        
        # Create ATSResult
        ats_result = ATSResult(
            candidate_id=candidate_id,
            ats_score=ats_result_dict['ats_score'],
            passed=ats_result_dict['passed'],
            skill_match_score=ats_result_dict['skill_match_score'],
            education_score=ats_result_dict['education_score'],
            experience_score=ats_result_dict['experience_score'],
            keyword_match_score=ats_result_dict['keyword_match_score'],
            format_score=ats_result_dict['format_score'],
            matched_skills=ats_result_dict['matched_skills'],
            missing_skills=ats_result_dict['missing_skills'],
            recommendations=[]
        )
        
        # Generate feedback if rejected
        feedback = None
        message = ""
        
        if not ats_result.passed:
            try:
                feedback_dict = feedback_generator.generate_feedback(
                    ats_result_dict, parsed_resume, job_req
                )
                
                if feedback_dict:
                    feedback = RejectionFeedback(
                        candidate_id=candidate_id,
                        ats_score=ats_result.ats_score,
                        minimum_required_score=job_req.minimum_ats_score,
                        rejection_reasons=feedback_dict['rejection_reasons'],
                        missing_critical_skills=feedback_dict['missing_critical_skills'],
                        resume_strengths=feedback_dict['resume_strengths'],
                        resume_weaknesses=feedback_dict['resume_weaknesses'],
                        improvement_recommendations=feedback_dict['improvement_recommendations'],
                        format_issues=feedback_dict['format_issues'],
                        mistake_highlights=feedback_dict['mistake_highlights']
                    )
                    
                    message = (
                        f"Candidate rejected. ATS Score: {ats_result.ats_score:.2f}% "
                        f"(Minimum Required: {job_req.minimum_ats_score}%). "
                        f"Feedback provided."
                    )
            except Exception as e:
                message = f"Candidate rejected. Error generating feedback: {str(e)}"
        else:
            message = (
                f"Candidate PASSED! ATS Score: {ats_result.ats_score:.2f}% "
                f"(Minimum Required: {job_req.minimum_ats_score}%)."
            )
        
        response = CandidateEvaluationResponse(
            candidate_id=candidate_id,
            ats_result=ats_result,
            feedback=feedback,
            message=message
        )
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


