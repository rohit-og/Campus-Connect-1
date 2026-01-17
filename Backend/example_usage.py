"""
Example usage script for Campus Connect AI Engine
Demonstrates how to use the API to evaluate candidates
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"


def example_with_resume_text():
    """Example: Evaluate candidate using resume text"""
    
    # Sample job requirement
    job_requirement = {
        "job_title": "Software Engineer",
        "required_skills": ["Python", "FastAPI", "SQL", "REST API"],
        "preferred_skills": ["Docker", "AWS", "React", "PostgreSQL"],
        "education_level": "Bachelor's",
        "years_of_experience": 2,
        "job_description": "We are looking for an experienced Software Engineer with strong Python skills and REST API development experience. The candidate should have experience with database design and modern web frameworks.",
        "keywords": ["API", "backend", "database", "web development", "Python"],
        "minimum_ats_score": 60.0
    }
    
    # Sample resume text
    resume_text = """
    JOHN DOE
    Email: john.doe@example.com
    Phone: +1-234-567-8900
    
    SKILLS
    Python, FastAPI, SQL, PostgreSQL, Docker, Git, REST API, JavaScript, React
    
    EDUCATION
    Bachelor of Science in Computer Science
    XYZ University, 2020-2024
    GPA: 3.8/4.0
    
    EXPERIENCE
    Software Engineer Intern
    ABC Tech Company, Summer 2023 - Present (1.5 years)
    - Developed REST APIs using Python and FastAPI
    - Designed and implemented database schemas using PostgreSQL
    - Collaborated with team using Git and Agile methodologies
    - Deployed applications using Docker containers
    
    Web Developer
    DEF Startup, 2022-2023 (1 year)
    - Built responsive web applications using React and JavaScript
    - Integrated REST APIs for data fetching
    
    PROJECTS
    E-commerce API: Built a complete REST API for an e-commerce platform using FastAPI and PostgreSQL
    Task Management App: Developed a full-stack application using React and Python backend
    """
    
    # Prepare payload
    payload = {
        "job_requirement": job_requirement,
        "resume_text": resume_text
    }
    
    # Make request
    print("Evaluating candidate with resume text...")
    response = requests.post(
        f"{BASE_URL}/api/v1/evaluate-json",
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "="*60)
        print("EVALUATION RESULT")
        print("="*60)
        print(f"\nCandidate ID: {result['candidate_id']}")
        print(f"ATS Score: {result['ats_result']['ats_score']}%")
        print(f"Status: {'✅ PASSED' if result['ats_result']['passed'] else '❌ REJECTED'}")
        print(f"\nScore Breakdown:")
        print(f"  - Skill Match: {result['ats_result']['skill_match_score']}%")
        print(f"  - Education: {result['ats_result']['education_score']}%")
        print(f"  - Experience: {result['ats_result']['experience_score']}%")
        print(f"  - Keyword Match: {result['ats_result']['keyword_match_score']}%")
        print(f"  - Format: {result['ats_result']['format_score']}%")
        
        if result['ats_result']['matched_skills']:
            print(f"\n✅ Matched Skills: {', '.join(result['ats_result']['matched_skills'][:5])}")
        
        if result['ats_result']['missing_skills']:
            print(f"\n❌ Missing Skills: {', '.join(result['ats_result']['missing_skills'][:5])}")
        
        # Show feedback if rejected
        if result['feedback']:
            print("\n" + "="*60)
            print("DETAILED FEEDBACK")
            print("="*60)
            print("\n📋 Rejection Reasons:")
            for i, reason in enumerate(result['feedback']['rejection_reasons'], 1):
                print(f"  {i}. {reason}")
            
            if result['feedback']['missing_critical_skills']:
                print("\n🔴 Missing Critical Skills:")
                for skill in result['feedback']['missing_critical_skills']:
                    print(f"  - {skill}")
            
            print("\n✅ Resume Strengths:")
            for strength in result['feedback']['resume_strengths'][:3]:
                print(f"  - {strength}")
            
            print("\n⚠️ Resume Weaknesses:")
            for weakness in result['feedback']['resume_weaknesses'][:3]:
                print(f"  - {weakness}")
            
            print("\n💡 Improvement Recommendations:")
            for i, rec in enumerate(result['feedback']['improvement_recommendations'][:5], 1):
                print(f"  {i}. {rec}")
            
            if result['feedback']['mistake_highlights']:
                print("\n🚨 Mistakes to Fix:")
                for mistake in result['feedback']['mistake_highlights'][:3]:
                    print(f"  - {mistake}")
        
        print("\n" + "="*60)
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def example_with_file():
    """Example: Evaluate candidate using resume file upload"""
    
    job_requirement = {
        "job_title": "Data Scientist",
        "required_skills": ["Python", "Machine Learning", "SQL", "Data Analysis"],
        "preferred_skills": ["TensorFlow", "Pandas", "NumPy", "Scikit-learn"],
        "education_level": "Master's",
        "years_of_experience": 1,
        "minimum_ats_score": 55.0,
        "keywords": ["data science", "ML", "statistics", "analytics"]
    }
    
    # Note: Replace 'resume.pdf' with actual path to resume file
    print("To use file upload, uncomment and modify this section:")
    print("with open('resume.pdf', 'rb') as f:")
    print("    files = {'resume_file': f}")
    print("    data = {'job_requirement': json.dumps(job_requirement)}")
    print("    response = requests.post(f'{BASE_URL}/api/v1/evaluate', files=files, data=data)")
    
    # Uncomment below to use with actual file:
    # with open('resume.pdf', 'rb') as f:
    #     files = {'resume_file': f}
    #     data = {'job_requirement': json.dumps(job_requirement)}
    #     response = requests.post(f'{BASE_URL}/api/v1/evaluate', files=files, data=data)
    #     print(response.json())


def check_health():
    """Check if the API server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API server is running!")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print(f"❌ API server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on http://localhost:8000")
        print("\nTo start the server, run:")
        print("  python main.py")
        print("  or")
        print("  uvicorn main:app --reload")
        return False


if __name__ == "__main__":
    print("Campus Connect AI Engine - Example Usage\n")
    
    # Check if server is running
    if not check_health():
        exit(1)
    
    print("\n")
    
    # Run example with resume text
    example_with_resume_text()
    
    print("\n\nNote: To use file upload, see the example_with_file() function")


