"""
Test script with dummy student resume data
Tests the ATS engine with sample student resumes
"""

import sys

# Check if required packages are installed
try:
    import pydantic
except ImportError:
    print("ERROR: pydantic is not installed.")
    print("Please run: pip install -r requirements.txt")
    print(f"Python executable: {sys.executable}")
    sys.exit(1)

try:
    import fastapi
except ImportError:
    print("ERROR: fastapi is not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# Now import project modules
import json
from models import JobRequirement, ResumeData
from resume_parser import ResumeParser
from ats_engine import ATSEngine
from feedback_generator import FeedbackGenerator

# Dummy resume data for students
DUMMY_RESUMES = {
    "varij_nayan_mishra": """
VARIJ NAYAN MISHRA
Email: varij.mishra@example.com
Phone: +91-9876543210
Location: Mumbai, India

SKILLS
Python, FastAPI, REST API, SQL, PostgreSQL, Docker, Git, JavaScript, React, 
Machine Learning, Data Analysis, Pandas, NumPy, Problem Solving

EDUCATION
Bachelor of Technology in Computer Science
Mumbai University, 2021-2025
CGPA: 8.5/10

Master of Science in Data Science (Pursuing)
IIT Mumbai, 2025-Present

EXPERIENCE
Software Development Intern
Tech Solutions Inc., June 2024 - December 2024 (6 months)
- Developed REST APIs using Python and FastAPI framework
- Worked with PostgreSQL database for data management
- Implemented authentication and authorization systems
- Collaborated in Agile development environment

Backend Developer (Part-time)
StartupXYZ, January 2024 - May 2024 (5 months)
- Built microservices architecture using FastAPI
- Designed database schemas and optimized queries
- Integrated third-party APIs for payment processing

PROJECTS
E-commerce API Platform
- Built complete REST API using FastAPI and PostgreSQL
- Implemented JWT authentication, order management system
- Deployed using Docker containers on AWS
Technologies: Python, FastAPI, PostgreSQL, Docker, AWS

Machine Learning Prediction System
- Developed ML model for predictive analytics
- Used scikit-learn for model training and evaluation
Technologies: Python, Machine Learning, Pandas, NumPy

CERTIFICATIONS
- AWS Certified Cloud Practitioner
- Python for Data Science (Coursera)
- REST API Development (Udemy)
""",

    "rohit_sharma": """
ROHIT SHARMA
Email: rohit.sharma@example.com
Phone: +91-8765432109
Location: Delhi, India

SKILLS
Java, Spring Boot, Hibernate, MySQL, MongoDB, JavaScript, Angular, 
Web Development, REST API, Microservices, Git, Linux, Docker

EDUCATION
Bachelor of Engineering in Computer Science
Delhi Technical University, 2020-2024
Percentage: 82%

EXPERIENCE
Software Engineer
Infotech Solutions Ltd., July 2024 - Present (6 months)
- Developed enterprise applications using Spring Boot framework
- Worked with MySQL and MongoDB databases
- Created RESTful web services and API endpoints
- Participated in code reviews and testing procedures

Java Developer Intern
GlobalTech Corp., January 2024 - June 2024 (6 months)
- Assisted in developing web applications using Java and Spring
- Performed database operations and query optimization
- Gained experience in Agile methodologies

PROJECTS
Employee Management System
- Full-stack application with Spring Boot backend and Angular frontend
- Features include CRUD operations, authentication, reporting
Technologies: Java, Spring Boot, Angular, MySQL

E-Learning Platform
- Online course management system with user dashboard
- Payment integration and certificate generation
Technologies: Spring Boot, MongoDB, React, Stripe API

CERTIFICATIONS
- Oracle Certified Java Programmer
- Spring Framework Certification
""",

    "ahana_basak": """
AHANA BASAK
Email: ahana.basak@example.com
Phone: +91-7654321098
Location: Kolkata, India

SKILLS
Python, Django, Flask, HTML, CSS, JavaScript, Bootstrap, SQL, 
Database Design, Web Development, API Development, Git, Responsive Design

EDUCATION
Bachelor of Science in Computer Science
Jadavpur University, 2021-2025
CGPA: 7.8/10

EXPERIENCE
Web Developer Intern
Digital Creations Pvt. Ltd., March 2024 - August 2024 (6 months)
- Developed responsive web applications using Django framework
- Designed and implemented database models
- Created REST APIs for frontend integration
- Worked on frontend development using HTML, CSS, JavaScript

Freelance Web Developer
June 2023 - February 2024 (9 months)
- Designed and developed websites for small businesses
- Implemented content management systems
- Provided maintenance and support services

PROJECTS
Blog Platform
- Full-featured blog application with user authentication
- Comments, likes, and admin panel functionality
Technologies: Django, PostgreSQL, Bootstrap, JavaScript

Task Management App
- Web-based task tracking application with team collaboration
- Real-time updates and notifications
Technologies: Django, SQLite, AJAX, jQuery

CERTIFICATIONS
- Django Web Framework Certification
- Full Stack Web Development Bootcamp
""",

    "sunipa_bose": """
SUNIPA BOSE
Email: sunipa.bose@example.com
Phone: +91-6543210987
Location: Bangalore, India

SKILLS
JavaScript, React, Node.js, Express.js, MongoDB, HTML5, CSS3, 
TypeScript, Redux, REST API, GraphQL, Git, Responsive Design, UI/UX

EDUCATION
Bachelor of Technology in Information Technology
Bangalore Institute of Technology, 2022-2026
CGPA: 8.2/10

EXPERIENCE
Frontend Developer Intern
WebTech Innovations, May 2024 - November 2024 (7 months)
- Developed user interfaces using React and TypeScript
- Built reusable components and implemented state management with Redux
- Integrated REST APIs and GraphQL endpoints
- Collaborated with UI/UX designers for responsive designs

Web Development Intern
CodeCraft Solutions, December 2023 - April 2024 (5 months)
- Created responsive web pages using HTML, CSS, JavaScript
- Worked on frontend frameworks and libraries
- Assisted in testing and debugging web applications

PROJECTS
Social Media Dashboard
- Real-time dashboard application with React and Redux
- Data visualization using charts and graphs
- Real-time notifications and updates
Technologies: React, Redux, Node.js, MongoDB, Chart.js

E-Commerce Frontend
- Complete shopping interface with cart and checkout
- User authentication and product search functionality
Technologies: React, TypeScript, Material-UI, REST API

CERTIFICATIONS
- React Developer Certification (Meta)
- Full Stack Web Development Specialization
- JavaScript Algorithms and Data Structures
"""
}

# Sample job requirements
JOB_REQUIREMENTS = {
    "backend_developer": {
        "job_title": "Backend Developer",
        "required_skills": ["Python", "FastAPI", "REST API", "SQL", "Git"],
        "preferred_skills": ["Docker", "PostgreSQL", "AWS", "Microservices"],
        "education_level": "Bachelor's",
        "years_of_experience": 1,
        "job_description": "We are looking for a skilled Backend Developer with experience in Python and FastAPI. The candidate should have strong knowledge of REST API development, database design, and cloud deployment.",
        "keywords": ["backend", "API", "database", "cloud", "microservices"],
        "minimum_ats_score": 60.0
    },
    
    "fullstack_developer": {
        "job_title": "Full Stack Developer",
        "required_skills": ["JavaScript", "React", "Node.js", "REST API", "Database"],
        "preferred_skills": ["TypeScript", "MongoDB", "Express.js", "GraphQL"],
        "education_level": "Bachelor's",
        "years_of_experience": 0,
        "job_description": "Looking for a Full Stack Developer proficient in JavaScript, React, and Node.js. Experience with databases and API development is required.",
        "keywords": ["fullstack", "javascript", "react", "node", "web development"],
        "minimum_ats_score": 55.0
    },
    
    "python_developer": {
        "job_title": "Python Developer",
        "required_skills": ["Python", "Web Framework", "Database", "API"],
        "preferred_skills": ["Django", "Flask", "FastAPI", "PostgreSQL"],
        "education_level": "Bachelor's",
        "years_of_experience": 0,
        "job_description": "Seeking a Python Developer with knowledge of web frameworks. Strong problem-solving skills and database experience preferred.",
        "keywords": ["python", "web development", "database", "framework"],
        "minimum_ats_score": 50.0
    }
}


def test_candidate(student_name, resume_text, job_req_dict):
    """Test a candidate against a job requirement"""
    print(f"\n{'='*70}")
    print(f"Testing: {student_name.upper()}")
    print(f"Job: {job_req_dict['job_title']}")
    print(f"{'='*70}")
    
    # Parse resume
    parser = ResumeParser()
    parsed_resume = parser.parse(resume_text=resume_text)
    resume_data = ResumeData(**parsed_resume)
    
    # Create job requirement
    job_req = JobRequirement(**job_req_dict)
    
    # Score resume
    ats_engine = ATSEngine()
    ats_result = ats_engine.score_resume(resume_data, job_req)
    
    # Display results
    print(f"\n[ATS SCORE: {ats_result['ats_score']:.2f}%]")
    print(f"Status: {'PASSED' if ats_result['passed'] else 'REJECTED'}")
    print(f"Minimum Required: {job_req.minimum_ats_score}%")
    
    print(f"\nScore Breakdown:")
    print(f"  - Skill Match:     {ats_result['skill_match_score']:.1f}%")
    print(f"  - Education:       {ats_result['education_score']:.1f}%")
    print(f"  - Experience:      {ats_result['experience_score']:.1f}%")
    print(f"  - Keyword Match:   {ats_result['keyword_match_score']:.1f}%")
    print(f"  - Format:          {ats_result['format_score']:.1f}%")
    
    if ats_result['matched_skills']:
        print(f"\nMatched Skills: {', '.join(ats_result['matched_skills'][:8])}")
    
    if ats_result['missing_skills']:
        print(f"Missing Skills: {', '.join(ats_result['missing_skills'][:5])}")
    
    # Generate feedback if rejected
    if not ats_result['passed']:
        feedback_gen = FeedbackGenerator()
        feedback = feedback_gen.generate_feedback(ats_result, parsed_resume, job_req)
        
        if feedback:
            print(f"\n{'='*70}")
            print("REJECTION FEEDBACK")
            print(f"{'='*70}")
            
            print("\nRejection Reasons:")
            for i, reason in enumerate(feedback['rejection_reasons'][:3], 1):
                print(f"  {i}. {reason}")
            
            if feedback['missing_critical_skills']:
                print(f"\nMissing Critical Skills: {', '.join(feedback['missing_critical_skills'])}")
            
            print("\nTop Recommendations:")
            for i, rec in enumerate(feedback['improvement_recommendations'][:3], 1):
                print(f"  {i}. {rec[:100]}...")
    
    return ats_result


def main():
    """Main test function"""
    print("="*70)
    print("CAMPUS CONNECT AI ENGINE - DUMMY DATA TEST")
    print("="*70)
    print("\nTesting 4 students against different job requirements")
    print("\nStudents:")
    print("  1. Varij Nayan Mishra")
    print("  2. Rohit Sharma")
    print("  3. Ahana Basak")
    print("  4. Sunipa Bose")
    
    # Test each candidate
    results = {}
    
    # Test 1: Backend Developer position
    print(f"\n\n{'#'*70}")
    print("# TEST 1: BACKEND DEVELOPER POSITION")
    print(f"{'#'*70}")
    
    job_req = JOB_REQUIREMENTS["backend_developer"]
    
    results["varij"] = test_candidate(
        "Varij Nayan Mishra", 
        DUMMY_RESUMES["varij_nayan_mishra"], 
        job_req
    )
    
    results["rohit"] = test_candidate(
        "Rohit Sharma", 
        DUMMY_RESUMES["rohit_sharma"], 
        job_req
    )
    
    results["ahana"] = test_candidate(
        "Ahana Basak", 
        DUMMY_RESUMES["ahana_basak"], 
        job_req
    )
    
    results["sunipa"] = test_candidate(
        "Sunipa Bose", 
        DUMMY_RESUMES["sunipa_bose"], 
        job_req
    )
    
    # Test 2: Full Stack Developer position
    print(f"\n\n{'#'*70}")
    print("# TEST 2: FULL STACK DEVELOPER POSITION")
    print(f"{'#'*70}")
    
    job_req = JOB_REQUIREMENTS["fullstack_developer"]
    
    test_candidate("Sunipa Bose", DUMMY_RESUMES["sunipa_bose"], job_req)
    test_candidate("Ahana Basak", DUMMY_RESUMES["ahana_basak"], job_req)
    
    # Test 3: Python Developer position
    print(f"\n\n{'#'*70}")
    print("# TEST 3: PYTHON DEVELOPER POSITION")
    print(f"{'#'*70}")
    
    job_req = JOB_REQUIREMENTS["python_developer"]
    
    test_candidate("Varij Nayan Mishra", DUMMY_RESUMES["varij_nayan_mishra"], job_req)
    test_candidate("Ahana Basak", DUMMY_RESUMES["ahana_basak"], job_req)
    
    # Summary
    print(f"\n\n{'='*70}")
    print("SUMMARY - BACKEND DEVELOPER POSITION")
    print(f"{'='*70}")
    print(f"\n{'Student Name':<25} {'ATS Score':<12} {'Status':<10}")
    print("-"*70)
    print(f"{'Varij Nayan Mishra':<25} {results['varij']['ats_score']:<12.2f} {'PASSED' if results['varij']['passed'] else 'REJECTED':<10}")
    print(f"{'Rohit Sharma':<25} {results['rohit']['ats_score']:<12.2f} {'PASSED' if results['rohit']['passed'] else 'REJECTED':<10}")
    print(f"{'Ahana Basak':<25} {results['ahana']['ats_score']:<12.2f} {'PASSED' if results['ahana']['passed'] else 'REJECTED':<10}")
    print(f"{'Sunipa Bose':<25} {results['sunipa']['ats_score']:<12.2f} {'PASSED' if results['sunipa']['passed'] else 'REJECTED':<10}")
    
    print(f"\n{'='*70}")
    print("Test completed successfully!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()

