"""
Database seeding script
Seeds the database with dummy data from test_dummy_data.py
"""

import sys
from datetime import datetime

# Import project modules
from database.postgres import SessionLocal, engine, Base
from database.mongodb import get_mongo_db
from database.models import User, Candidate, Job, Application, UserRole, ApplicationStatus
from auth.password import get_password_hash
from resume_parser import ResumeParser
from test_dummy_data import DUMMY_RESUMES, JOB_REQUIREMENTS

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)


def seed_users_and_candidates(db):
    """Seed users and candidates from dummy resumes"""
    print("Seeding users and candidates...")
    
    # Get MongoDB connection
    try:
        mongo_db = get_mongo_db()
    except Exception as e:
        print(f"Warning: MongoDB connection failed: {e}")
        print("Resumes will not be stored in MongoDB, but candidates will still be created.")
        mongo_db = None
    
    parser = ResumeParser()
    created_users = {}
    created_candidates = {}
    
    # Student data mapping
    student_data = {
        "varij_nayan_mishra": {
            "name": "Varij Nayan Mishra",
            "email": "varij.mishra@example.com",
            "password": "password123"
        },
        "rohit_sharma": {
            "name": "Rohit Sharma",
            "email": "rohit.sharma@example.com",
            "password": "password123"
        },
        "ahana_basak": {
            "name": "Ahana Basak",
            "email": "ahana.basak@example.com",
            "password": "password123"
        },
        "sunipa_bose": {
            "name": "Sunipa Bose",
            "email": "sunipa.bose@example.com",
            "password": "password123"
        }
    }
    
    for key, resume_text in DUMMY_RESUMES.items():
        student_info = student_data.get(key)
        if not student_info:
            continue
        
        # Parse resume
        parsed_resume = parser.parse(resume_text=resume_text)
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == student_info["email"]).first()
        if existing_user:
            print(f"  User {student_info['email']} already exists, skipping...")
            created_users[key] = existing_user
            # Get existing candidate
            candidate = db.query(Candidate).filter(Candidate.user_id == existing_user.id).first()
            if candidate:
                created_candidates[key] = candidate
            continue
        
        # Create user
        user = User(
            email=student_info["email"],
            password_hash=get_password_hash(student_info["password"]),
            role=UserRole.STUDENT
        )
        db.add(user)
        db.flush()  # Flush to get user.id
        
        created_users[key] = user
        print(f"  Created user: {student_info['email']} (ID: {user.id})")
        
        # Store resume in MongoDB
        resume_id = None
        if mongo_db is not None:
            try:
                resume_doc = {
                    "user_id": user.id,
                    "parsed_data": parsed_resume,
                    "raw_text": resume_text,
                    "created_at": datetime.utcnow()
                }
                result = mongo_db.resumes.insert_one(resume_doc)
                resume_id = str(result.inserted_id)
                print(f"    Stored resume in MongoDB: {resume_id}")
            except Exception as e:
                print(f"    Warning: Failed to store resume in MongoDB: {e}")
        
        # Create candidate
        candidate = Candidate(
            user_id=user.id,
            name=student_info["name"],
            email=student_info["email"],
            phone=parsed_resume.get("phone"),
            skills_json=parsed_resume.get("skills", []),
            resume_id=resume_id
        )
        db.add(candidate)
        db.flush()
        
        created_candidates[key] = candidate
        print(f"  Created candidate: {student_info['name']} (ID: {candidate.id})")
    
    # Create a recruiter user for job postings
    recruiter_email = "recruiter@example.com"
    existing_recruiter = db.query(User).filter(User.email == recruiter_email).first()
    if existing_recruiter:
        print(f"  Recruiter {recruiter_email} already exists, using existing...")
        recruiter_user = existing_recruiter
    else:
        recruiter_user = User(
            email=recruiter_email,
            password_hash=get_password_hash("recruiter123"),
            role=UserRole.RECRUITER
        )
        db.add(recruiter_user)
        db.flush()
        print(f"  Created recruiter: {recruiter_email} (ID: {recruiter_user.id})")
    
    db.commit()
    print(f"✓ Seeded {len(created_users)} users and {len(created_candidates)} candidates\n")
    
    return created_users, created_candidates, recruiter_user


def seed_jobs(db, recruiter_user):
    """Seed job postings from job requirements"""
    print("Seeding job postings...")
    
    created_jobs = {}
    
    # Company names for each job
    companies = {
        "backend_developer": "Tech Solutions Inc.",
        "fullstack_developer": "WebTech Innovations",
        "python_developer": "Python Solutions Ltd."
    }
    
    for key, job_req in JOB_REQUIREMENTS.items():
        # Check if job already exists
        existing_job = db.query(Job).filter(
            Job.title == job_req["job_title"],
            Job.company == companies.get(key, "Tech Company")
        ).first()
        
        if existing_job:
            print(f"  Job '{job_req['job_title']}' already exists, skipping...")
            created_jobs[key] = existing_job
            continue
        
        # Create job posting
        job = Job(
            title=job_req["job_title"],
            company=companies.get(key, "Tech Company"),
            description=job_req.get("job_description", ""),
            location="Remote / Multiple Locations",
            salary="Competitive",
            requirements_json=job_req,  # Store entire job requirement as JSON
            created_by=recruiter_user.id
        )
        db.add(job)
        db.flush()
        
        created_jobs[key] = job
        print(f"  Created job: {job_req['job_title']} at {job.company} (ID: {job.id})")
    
    db.commit()
    print(f"✓ Seeded {len(created_jobs)} job postings\n")
    
    return created_jobs


def seed_applications(db, candidates, jobs):
    """Seed some sample applications"""
    print("Seeding applications...")
    
    # Map candidates to jobs they might apply for
    # Based on the test scenarios in test_dummy_data.py
    applications_map = [
        # Backend Developer position - all candidates
        ("varij_nayan_mishra", "backend_developer"),
        ("rohit_sharma", "backend_developer"),
        ("ahana_basak", "backend_developer"),
        ("sunipa_bose", "backend_developer"),
        # Full Stack Developer position
        ("sunipa_bose", "fullstack_developer"),
        ("ahana_basak", "fullstack_developer"),
        # Python Developer position
        ("varij_nayan_mishra", "python_developer"),
        ("ahana_basak", "python_developer"),
    ]
    
    created_count = 0
    for candidate_key, job_key in applications_map:
        if candidate_key not in candidates or job_key not in jobs:
            continue
        
        candidate = candidates[candidate_key]
        job = jobs[job_key]
        
        # Check if application already exists
        existing_app = db.query(Application).filter(
            Application.candidate_id == candidate.id,
            Application.job_id == job.id
        ).first()
        
        if existing_app:
            continue
        
        # Create application
        application = Application(
            job_id=job.id,
            candidate_id=candidate.id,
            status=ApplicationStatus.PENDING
        )
        db.add(application)
        created_count += 1
        print(f"  Created application: {candidate.name} -> {job.title}")
    
    db.commit()
    print(f"✓ Seeded {created_count} applications\n")


def main():
    """Main seeding function"""
    print("="*70)
    print("CAMPUS CONNECT - DATABASE SEEDING")
    print("="*70)
    print()
    
    db = SessionLocal()
    
    try:
        # Seed users and candidates
        users, candidates, recruiter = seed_users_and_candidates(db)
        
        # Seed jobs
        jobs = seed_jobs(db, recruiter)
        
        # Seed applications
        seed_applications(db, candidates, jobs)
        
        print("="*70)
        print("✓ Database seeding completed successfully!")
        print("="*70)
        print("\nSummary:")
        print(f"  - Users created: {len(users)} students + 1 recruiter")
        print(f"  - Candidates created: {len(candidates)}")
        print(f"  - Jobs created: {len(jobs)}")
        print("\nLogin credentials:")
        print("  Students:")
        for key, user in users.items():
            print(f"    Email: {user.email}, Password: password123")
        print(f"  Recruiter:")
        print(f"    Email: recruiter@example.com, Password: recruiter123")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
