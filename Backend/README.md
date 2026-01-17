# Campus Connect AI Engine

An AI-powered Applicant Tracking System (ATS) and Feedback Generator for Campus Connect - a platform that bridges colleges and companies for recruitment.

## Features

### 1. ATS Resume Screening
- **Resume Parsing**: Extracts information from PDF and DOCX resume files
- **Multi-criteria Scoring**: Evaluates candidates based on:
  - Skill matching (required & preferred skills)
  - Education level alignment
  - Years of experience
  - Keyword relevance
  - Resume format and structure
- **Configurable Threshold**: Recruiters can set minimum ATS score required

### 2. Real-time Feedback System
For rejected candidates, the system provides:
- **Rejection Reasons**: Specific reasons why the candidate was rejected
- **Missing Skills**: List of critical skills that are missing
- **Resume Strengths**: What the resume does well
- **Resume Weaknesses**: Areas that need improvement
- **Actionable Recommendations**: Step-by-step suggestions to improve the resume
- **Mistake Highlights**: Specific mistakes found in the resume

## Tech Stack

- **Python 3.8+**
- **FastAPI** - Modern, fast web framework for building APIs
- **PyPDF2 / pdfplumber** - PDF parsing
- **python-docx** - DOCX parsing
- **Pydantic** - Data validation and serialization

## Installation

1. **Clone the repository** (or navigate to project directory)

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```


## Usage

### Starting the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API Docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Docs (ReDoc)**: `http://localhost:8000/redoc`

### Example API Request

#### Using Form Data (with file upload):

```python
import requests

# Job requirements
job_requirement = {
    "job_title": "Software Engineer",
    "required_skills": ["Python", "FastAPI", "SQL"],
    "preferred_skills": ["Docker", "AWS", "React"],
    "education_level": "Bachelor's",
    "years_of_experience": 2,
    "job_description": "We are looking for a skilled software engineer...",
    "keywords": ["API", "backend", "database"],
    "minimum_ats_score": 60.0
}

# Make request
files = {'resume_file': open('resume.pdf', 'rb')}
data = {'job_requirement': json.dumps(job_requirement)}

response = requests.post('http://localhost:8000/api/v1/evaluate', files=files, data=data)
print(response.json())
```

#### Using JSON (with resume text):

```python
import requests
import json

payload = {
    "job_requirement": {
        "job_title": "Software Engineer",
        "required_skills": ["Python", "FastAPI"],
        "preferred_skills": ["Docker"],
        "education_level": "Bachelor's",
        "years_of_experience": 2,
        "minimum_ats_score": 60.0,
        "keywords": ["API", "backend"]
    },
    "resume_text": """
    John Doe
    Email: john@example.com
    Phone: 123-456-7890
    
    Skills: Python, FastAPI, SQL, Docker
    
    Education:
    Bachelor's in Computer Science, XYZ University
    
    Experience:
    Software Engineer at ABC Corp (2 years)
    """
}

response = requests.post(
    'http://localhost:8000/api/v1/evaluate-json',
    json=payload
)
print(json.dumps(response.json(), indent=2))
```

### Example Response

**When Candidate Passes:**
```json
{
  "candidate_id": "uuid-here",
  "ats_result": {
    "candidate_id": "uuid-here",
    "ats_score": 75.5,
    "passed": true,
    "skill_match_score": 85.0,
    "education_score": 100.0,
    "experience_score": 80.0,
    "keyword_match_score": 70.0,
    "format_score": 95.0,
    "matched_skills": ["Python", "FastAPI", "SQL"],
    "missing_skills": []
  },
  "feedback": null,
  "message": "Candidate PASSED! ATS Score: 75.50% (Minimum Required: 60.00%)."
}
```

**When Candidate is Rejected:**
```json
{
  "candidate_id": "uuid-here",
  "ats_result": {
    "ats_score": 45.2,
    "passed": false,
    ...
  },
  "feedback": {
    "candidate_id": "uuid-here",
    "ats_score": 45.2,
    "minimum_required_score": 60.0,
    "rejection_reasons": [
      "Insufficient skill match (40.0%). Missing 2 required skills.",
      "Low keyword relevance (35.0%)."
    ],
    "missing_critical_skills": ["FastAPI", "SQL"],
    "resume_strengths": [
      "Good skill alignment: 1 matching skills found"
    ],
    "resume_weaknesses": [
      "Limited skills listed - expand your skills section"
    ],
    "improvement_recommendations": [
      "Add these required skills to your resume: FastAPI, SQL",
      "Review the job description and incorporate relevant keywords..."
    ],
    "mistake_highlights": [
      "Critical missing skills: FastAPI, SQL",
      "Experience section needs more detail"
    ]
  },
  "message": "Candidate rejected. Feedback provided."
}
```

## Project Structure

```
Campus Connect/
├── main.py                 # FastAPI application and endpoints
├── models.py               # Pydantic models for API requests/responses
├── resume_parser.py        # Resume parsing logic (PDF/DOCX)
├── ats_engine.py           # ATS scoring engine
├── feedback_generator.py   # Feedback generation for rejected candidates
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── uploads/               # Temporary directory for uploaded files (auto-created)
```

## How It Works

### 1. Resume Parsing
- Extracts contact information (name, email, phone)
- Identifies skills, education, experience, certifications, projects
- Parses raw text for keyword matching

### 2. ATS Scoring (Weighted)
- **Skills (40%)**: Matches required and preferred skills
- **Keywords (25%)**: Relevance to job description
- **Experience (20%)**: Years of experience alignment
- **Education (10%)**: Education level matching
- **Format (5%)**: Resume structure and completeness

### 3. Feedback Generation
- Analyzes each scoring component
- Identifies specific gaps and weaknesses
- Provides actionable improvement recommendations
- Highlights mistakes and missing elements

## Customization

You can customize the scoring weights in `ats_engine.py` in the `_calculate_total_score` method.

## Error Handling

The API includes comprehensive error handling for:
- Invalid file formats
- Missing required fields
- Parsing errors
- Scoring calculation errors

## Notes

- Uploaded resume files are automatically cleaned up after processing
- The system supports both file upload and text input for resumes
- Minimum ATS score can be set per job requirement (default: 50.0)

## License

This project is part of Campus Connect.

## Support

For issues or questions, please contact the development team.


