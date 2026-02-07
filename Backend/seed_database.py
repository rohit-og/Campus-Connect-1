"""
Database seeding script
Seeds the database with dummy data from test_dummy_data.py.
Includes hackathon demo data: TPO, evaluations, badges, mentors, events,
prep modules, aptitude test, conversations, verification, placements.
"""

import sys
from datetime import datetime, timezone, timedelta

# Import project modules
from database.postgres import SessionLocal, engine, Base
from database.mongodb import get_mongo_db
from database.models import (
    User, Candidate, Job, Application, UserRole, ApplicationStatus,
    Evaluation, Badge, CandidateBadge, MentorProfile, MentorshipRequest,
    Event, EventRegistration, PrepModule, AptitudeTest, AptitudeQuestion,
    TestAttempt, Conversation, Message,
)
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


def seed_tpo_user(db):
    """Create TPO user for dashboard and verification demo."""
    print("Seeding TPO user...")
    email = "tpo@campusconnect.edu"
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print(f"  TPO {email} already exists, skipping...")
        return existing
    user = User(
        email=email,
        password_hash=get_password_hash("tpo123"),
        role=UserRole.TPO,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"  Created TPO: {email} (ID: {user.id})")
    print("✓ Seeded TPO user\n")
    return user


def seed_evaluations(db):
    """Create evaluations for all applications (enables HR pre-screened list and feedback)."""
    print("Seeding evaluations...")
    from routers.ats import create_evaluation_for_application
    applications = db.query(Application).all()
    count = 0
    for app in applications:
        ev = create_evaluation_for_application(app, db)
        if ev:
            count += 1
            print(f"  Evaluation for application {app.id} (candidate {app.candidate_id} -> job {app.job_id}): score={ev.ats_score:.1f}, passed={ev.passed}")
    print(f"✓ Seeded {count} evaluations\n")


def seed_badges(db, jobs):
    """Create skill badges and optionally award some (ATS already awards on pass)."""
    print("Seeding badges...")
    skill_badges = [
        ("Python Ninja", "Strong Python and backend skills", "python"),
        ("React Pro", "Frontend and React expertise", "react"),
        ("Backend Ready", "REST API and server-side development", "api"),
        ("Full Stack Star", "Full stack web development", "javascript"),
        ("Java Champion", "Java and enterprise development", "java"),
    ]
    created = {}
    for name, desc, skill_key in skill_badges:
        existing = db.query(Badge).filter(Badge.skill_key == skill_key).first()
        if existing:
            created[skill_key] = existing
            continue
        badge = Badge(
            name=name,
            description=desc,
            skill_key=skill_key,
            criteria_json={"min_score": 60},
        )
        db.add(badge)
        db.flush()
        created[skill_key] = badge
        print(f"  Created badge: {name} ({skill_key})")
    db.commit()
    # Award a couple of TPO badges for demo variety
    candidates = db.query(Candidate).limit(3).all()
    badge_list = list(created.values())
    for i, c in enumerate(candidates):
        if i >= len(badge_list):
            break
        b = badge_list[i]
        if db.query(CandidateBadge).filter(CandidateBadge.candidate_id == c.id, CandidateBadge.badge_id == b.id).first():
            continue
        cb = CandidateBadge(candidate_id=c.id, badge_id=b.id, source="tpo")
        db.add(cb)
        print(f"  Awarded {b.name} to {c.name} (TPO)")
    db.commit()
    print(f"✓ Seeded {len(created)} badges\n")


def seed_mentors(db, candidates_dict):
    """Create mentor users, profiles, and mentorship requests."""
    print("Seeding mentors and mentorship requests...")
    mentor_data = [
        ("mentor1@alumni.edu", "Senior Backend Engineer | Ex-FAANG", "Python, System Design, Career guidance", "Tech Solutions Inc.", 8),
        ("mentor2@alumni.edu", "Frontend Lead | React Specialist", "React, TypeScript, UI/UX", "WebTech Innovations", 6),
    ]
    mentors = []
    for email, headline, skills_str, company, years in mentor_data:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                password_hash=get_password_hash("mentor123"),
                role=UserRole.MENTOR,
            )
            db.add(user)
            db.flush()
        profile = db.query(MentorProfile).filter(MentorProfile.user_id == user.id).first()
        if profile:
            mentors.append(profile)
        else:
            skills = [s.strip() for s in skills_str.split(",")]
            profile = MentorProfile(
                user_id=user.id,
                headline=headline,
                bio="Alumni mentor happy to help with interviews and career advice.",
                skills_json=skills,
                company=company,
                years_experience=years,
                is_available=True,
            )
            db.add(profile)
            db.flush()
            mentors.append(profile)
        print(f"  Mentor: {email}")
    db.commit()

    # Mentorship requests from candidates
    candidate_list = list(candidates_dict.values()) if isinstance(candidates_dict, dict) else db.query(Candidate).limit(4).all()
    statuses = ["pending", "accepted", "declined"]
    for i, cand in enumerate(candidate_list):
        if i >= len(mentors):
            break
        mentor = mentors[i % len(mentors)]
        existing = db.query(MentorshipRequest).filter(
            MentorshipRequest.mentor_id == mentor.id,
            MentorshipRequest.student_id == cand.id,
        ).first()
        if existing:
            continue
        status = statuses[i % 3]
        req = MentorshipRequest(
            mentor_id=mentor.id,
            student_id=cand.id,
            message="I would like guidance on technical interviews.",
            status=status,
        )
        if status != "pending":
            req.responded_at = datetime.now(timezone.utc)
        db.add(req)
    db.commit()
    print(f"✓ Seeded {len(mentors)} mentors and mentorship requests\n")


def seed_events(db, candidates_dict):
    """Create hackathon/startup events and registrations."""
    print("Seeding events and registrations...")
    now = datetime.now(timezone.utc)
    events_data = [
        ("Campus Hackathon 2025", "48-hour hackathon for students. Build something cool!", "hackathon", 30),
        ("Startup Weekend", "Validate your idea in a weekend.", "startup", 50),
        ("API & Backend Workshop", "Hands-on REST APIs and databases.", "workshop", 40),
    ]
    created_events = []
    for title, desc, typ, max_p in events_data:
        existing = db.query(Event).filter(Event.title == title).first()
        if existing:
            created_events.append(existing)
            continue
        start = now + timedelta(days=14)
        end = start + timedelta(days=2) if typ == "hackathon" else start + timedelta(hours=8)
        event = Event(
            title=title,
            description=desc,
            type=typ,
            start_date=start,
            end_date=end,
            location="Main Campus / Hybrid",
            registration_deadline=now + timedelta(days=7),
            max_participants=max_p,
            is_active=True,
        )
        db.add(event)
        db.flush()
        created_events.append(event)
        print(f"  Event: {title} ({typ})")
    db.commit()

    candidate_list = list(candidates_dict.values()) if isinstance(candidates_dict, dict) else db.query(Candidate).limit(4).all()
    for event in created_events:
        for i, cand in enumerate(candidate_list):
            if i > 2:
                break
            existing = db.query(EventRegistration).filter(
                EventRegistration.event_id == event.id,
                EventRegistration.candidate_id == cand.id,
            ).first()
            if existing:
                continue
            reg = EventRegistration(event_id=event.id, candidate_id=cand.id, status="registered")
            db.add(reg)
    db.commit()
    print(f"✓ Seeded {len(created_events)} events and registrations\n")


def seed_prep_modules(db, jobs):
    """Create company/JD-specific prep content."""
    print("Seeding prep modules...")
    job_list = list(jobs.values()) if isinstance(jobs, dict) else db.query(Job).limit(5).all()
    prep_data = [
        ("Tech Solutions Inc. – Backend Interview Tips", "Tech Solutions Inc.", "company_tips",
         "Focus on REST design, SQL, and system design. They value clean code and testing."),
        ("WebTech – Full Stack Prep", "WebTech Innovations", "company_tips",
         "Be ready for a live coding round. React and Node are core. Know your async JS."),
        ("Backend Developer JD Checklist", None, "jd_checklist",
         "1. Revise REST and API design.\n2. Brush up PostgreSQL queries.\n3. Prepare STAR stories for teamwork."),
        ("Python Developer – Common Questions", "Python Solutions Ltd.", "company_tips",
         "Python data structures, decorators, and one system design question are typical."),
    ]
    for title, company, typ, content in prep_data:
        existing = db.query(PrepModule).filter(PrepModule.title == title).first()
        if existing:
            continue
        job_id = job_list[0].id if job_list and "Backend" in title else (job_list[1].id if job_list and "Full Stack" in title else None)
        mod = PrepModule(title=title, company=company, job_id=job_id, content=content, type=typ)
        db.add(mod)
        print(f"  Prep: {title}")
    db.commit()
    print("✓ Seeded prep modules\n")


def seed_aptitude(db, candidates_dict):
    """Create one aptitude test with questions and 2–3 test attempts."""
    print("Seeding aptitude test and attempts...")
    existing_test = db.query(AptitudeTest).filter(AptitudeTest.title == "General Aptitude – Demo").first()
    if existing_test:
        test = existing_test
    else:
        test = AptitudeTest(
            title="General Aptitude – Demo",
            description="Sample quantitative and logical reasoning for campus placements.",
            duration_minutes=30,
            is_active=True,
        )
        db.add(test)
        db.flush()
    questions_data = [
        ("If a train travels 120 km in 2 hours, what is its average speed?", ["50 km/h", "60 km/h", "70 km/h", "80 km/h"], 1, "quant", "easy"),
        ("What is the next number: 2, 6, 12, 20, 30, ?", ["38", "42", "44", "46"], 1, "quant", "medium"),
        ("If all roses are flowers and some flowers are red, which is definitely true?", ["All roses are red", "Some roses are red", "No roses are red", "Cannot be determined"], 3, "verbal", "medium"),
        ("A shopkeeper sells an item for $120 with 20% profit. Cost price?", ["$90", "$100", "$110", "$115"], 1, "quant", "medium"),
        ("Word closest in meaning to ABUNDANT:", ["Scarce", "Plentiful", "Limited", "Rare"], 1, "verbal", "easy"),
        ("If 3x + 5 = 20, then x = ?", ["3", "4", "5", "6"], 2, "quant", "easy"),
        ("In a code, CAT is 3120. What is DOG?", ["4157", "4158", "4159", "4160"], 0, "logical", "medium"),
        ("Which is the odd one out: Python, Java, HTML, C++?", ["Python", "Java", "HTML", "C++"], 2, "verbal", "easy"),
    ]
    if not existing_test:
        for q_text, options, correct_idx, category, difficulty in questions_data:
            q = AptitudeQuestion(
                test_id=test.id,
                question_text=q_text,
                options_json=options,
                correct_index=correct_idx,
                category=category,
                difficulty=difficulty,
            )
            db.add(q)
        db.commit()
        db.refresh(test)

    candidate_list = list(candidates_dict.values()) if isinstance(candidates_dict, dict) else db.query(Candidate).limit(3).all()
    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.test_id == test.id).all()
    question_ids = [q.id for q in questions]
    correct_index_by_qid = {q.id: q.correct_index for q in questions}
    if not question_ids:
        print("  No questions for test, skipping attempts.")
        print("✓ Aptitude seed done\n")
        return
    for i, cand in enumerate(candidate_list):
        existing_attempt = db.query(TestAttempt).filter(
            TestAttempt.test_id == test.id,
            TestAttempt.candidate_id == cand.id,
        ).first()
        if existing_attempt:
            continue
        # Simulate answers: mix correct and wrong so scores vary
        answers = {str(qid): (i + j) % 4 for j, qid in enumerate(question_ids)}
        correct_count = sum(
            1 for qid in question_ids
            if answers.get(str(qid)) == correct_index_by_qid.get(qid)
        )
        total = len(question_ids)
        score = (correct_count / total * 100) if total else 0
        passed = score >= 70
        attempt = TestAttempt(
            test_id=test.id,
            candidate_id=cand.id,
            submitted_at=datetime.now(timezone.utc),
            score=round(score, 2),
            passed=passed,
            answers_json=answers,
        )
        db.add(attempt)
        print(f"  Attempt: {cand.name} score={score:.1f}% passed={passed}")
    db.commit()
    print("✓ Seeded aptitude test and attempts\n")


def seed_conversations(db, recruiter_user, candidates_dict, jobs):
    """Create recruiter–candidate conversations with messages."""
    print("Seeding conversations and messages...")
    recruiter_id = recruiter_user.id if hasattr(recruiter_user, "id") else recruiter_user
    job_list = list(jobs.values()) if isinstance(jobs, dict) else db.query(Job).limit(3).all()
    candidate_list = list(candidates_dict.values()) if isinstance(candidates_dict, dict) else db.query(Candidate).limit(3).all()
    if not job_list or not candidate_list:
        print("  No jobs or candidates, skipping conversations.")
        print("✓ Conversations seed done\n")
        return
    convos = []
    for i, cand in enumerate(candidate_list):
        job = job_list[i % len(job_list)]
        existing = db.query(Conversation).filter(
            Conversation.job_id == job.id,
            Conversation.candidate_id == cand.id,
        ).first()
        if existing:
            continue
        conv = Conversation(job_id=job.id, company_user_id=recruiter_id, candidate_id=cand.id)
        db.add(conv)
        db.flush()
        convos.append((conv, cand, job))
    db.commit()

    msg_pairs = [
        ("Hi, we received your application for the {} role. When are you free for a short call?", "Thank you! I'm available this week."),
        ("How about Thursday 3 PM?", "Thursday 3 PM works for me."),
        ("Great. We'll send a calendar invite. Do you have any questions about the role?", "I wanted to ask about the team size and tech stack."),
    ]
    for conv, cand, job in convos:
        for j, (recruiter_msg, candidate_msg) in enumerate(msg_pairs):
            m1 = Message(conversation_id=conv.id, sender_id=recruiter_id, body=recruiter_msg.format(job.title))
            m2 = Message(conversation_id=conv.id, sender_id=cand.user_id, body=candidate_msg)
            db.add(m1)
            db.add(m2)
        print(f"  Conversation: {cand.name} <-> job {job.title}")
    db.commit()
    print("✓ Seeded conversations and messages\n")


def seed_verification_and_placements(db, tpo_user, candidates_dict, jobs):
    """Set some candidates TPO-verified and 1–2 applications as ACCEPTED."""
    print("Seeding TPO verification and placements...")
    tpo_id = tpo_user.id if hasattr(tpo_user, "id") else tpo_user
    candidate_list = list(candidates_dict.values()) if isinstance(candidates_dict, dict) else db.query(Candidate).all()
    # Verify all but last candidate
    for i, c in enumerate(candidate_list):
        if i < len(candidate_list) - 1:
            if not c.is_verified:
                c.is_verified = True
                c.verified_at = datetime.now(timezone.utc)
                c.verified_by = tpo_id
                print(f"  Verified: {c.name}")
        # else: leave one unverified for demo queue
    applications = db.query(Application).all()
    accepted = 0
    for app in applications:
        if accepted >= 2:
            break
        if app.status == ApplicationStatus.ACCEPTED:
            continue
        # Accept first 2 applications (e.g. Varij and Sunipa for backend/fullstack)
        app.status = ApplicationStatus.ACCEPTED
        accepted += 1
        print(f"  Placement: {app.candidate.name} -> job id {app.job_id}")
    db.commit()
    print(f"✓ Seeded verification and {accepted} placements\n")


def main():
    """Main seeding function (base + hackathon demo data)."""
    print("="*70)
    print("CAMPUS CONNECT - DATABASE SEEDING (BASE + HACKATHON DEMO)")
    print("="*70)
    print()

    db = SessionLocal()

    try:
        # 1. Base: users, candidates, recruiter
        users, candidates, recruiter = seed_users_and_candidates(db)
        jobs = seed_jobs(db, recruiter)
        seed_applications(db, candidates, jobs)

        # 2. TPO user
        tpo_user = seed_tpo_user(db)

        # 3. Evaluations for all applications (HR pre-screened, feedback)
        seed_evaluations(db)

        # 4. Badges (skill_key aligned to jobs; ATS already awards on pass)
        seed_badges(db, jobs)

        # 5. Mentors and mentorship requests
        seed_mentors(db, candidates)

        # 6. Events (hackathon, startup, workshop) and registrations
        seed_events(db, candidates)

        # 7. Prep modules (company/JD-specific)
        seed_prep_modules(db, jobs)

        # 8. Aptitude test + attempts
        seed_aptitude(db, candidates)

        # 9. Conversations and messages (company–candidate)
        seed_conversations(db, recruiter, candidates, jobs)

        # 10. TPO verification and placements
        seed_verification_and_placements(db, tpo_user, candidates, jobs)

        print("="*70)
        print("✓ Database seeding completed successfully!")
        print("="*70)
        print("\nSummary:")
        print(f"  - Users: {len(users)} students + 1 recruiter + 1 TPO + 2 mentors")
        print(f"  - Candidates: {len(candidates)}")
        print(f"  - Jobs: {len(jobs)}")
        print("\nLogin credentials (hackathon demo):")
        print("  Students:")
        for key, user in users.items():
            print(f"    {user.email} / password123")
        print("  Recruiter: recruiter@example.com / recruiter123")
        print("  TPO: tpo@campusconnect.edu / tpo123")
        print("  Mentors: mentor1@alumni.edu, mentor2@alumni.edu / mentor123")
        print("\nFor AI Skill Matchmaking: after seed, have an admin call POST /api/v1/vector/reindex/jobs")
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
