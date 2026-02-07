"""Analytics Q&A over recruitment data (safe, aggregate only)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.dependencies import get_current_active_user
from config import GROQ_API_KEY
from database.models import User, Job, Candidate, Application, Evaluation, ApplicationStatus
from database.postgres import get_db
from llm.groq_client import get_groq_client


router = APIRouter(prefix="/api/v1/llm/analytics", tags=["LLM - Analytics"])


def _require_admin_or_recruiter(user: User) -> None:
    if user.role.value not in ["recruiter", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Only recruiters and admins can query analytics.",
        )
    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY is not configured; analytics Q&A is unavailable.",
        )


def _compute_basic_metrics(db: Session) -> dict:
    """Aggregate a small, safe set of metrics for the LLM to reason over."""
    total_jobs = db.query(Job).count()
    total_candidates = db.query(Candidate).count()
    total_applications = db.query(Application).count()
    total_evaluations = db.query(Evaluation).count()

    status_counts = {}
    for status in ApplicationStatus:
        status_counts[status.value] = db.query(Application).filter(Application.status == status).count()

    # Per-job pass rates (limited)
    job_pass_stats = []
    jobs = db.query(Job).limit(50).all()
    for job in jobs:
        apps = db.query(Application).filter(Application.job_id == job.id).all()
        app_ids = [a.id for a in apps]
        if not app_ids:
            continue
        evals = db.query(Evaluation).filter(Evaluation.application_id.in_(app_ids)).all()
        if not evals:
            continue
        passed = sum(1 for e in evals if e.passed)
        failed = sum(1 for e in evals if not e.passed)
        job_pass_stats.append(
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "applications": len(apps),
                "passed": passed,
                "failed": failed,
            }
        )

    return {
        "totals": {
            "jobs": total_jobs,
            "candidates": total_candidates,
            "applications": total_applications,
            "evaluations": total_evaluations,
        },
        "application_status_counts": status_counts,
        "job_pass_stats": job_pass_stats,
    }


@router.post("/ask")
async def ask_analytics(
    question: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Natural-language Q&A over high-level recruitment analytics.

    The LLM only sees pre-aggregated metrics; it does not run arbitrary SQL.
    """
    _require_admin_or_recruiter(current_user)

    metrics = _compute_basic_metrics(db)

    client = get_groq_client()
    system_prompt = (
        "You are an analytics assistant for a recruitment platform. "
        "You receive a JSON blob with aggregate statistics and a natural language question. "
        "Answer based ONLY on the provided data.\n\n"
        "Always return valid JSON only with fields:\n"
        "- answer: string (natural language answer)\n"
        "- used_metrics: string[] (names of metrics you relied on)\n"
        "- caveats: string[] (optional limitations or notes)\n"
    )
    user_prompt = (
        f"Question: {question}\n\n"
        f"Aggregated metrics (JSON):\n{metrics}\n"
    )

    result = client.chat_json(system_prompt=system_prompt, user_prompt=user_prompt)

    return {
        "question": question,
        "answer": result.get("answer", ""),
        "used_metrics": result.get("used_metrics", []),
        "caveats": result.get("caveats", []),
        "metrics_snapshot": metrics,
    }

