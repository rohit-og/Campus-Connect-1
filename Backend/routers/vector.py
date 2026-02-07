"""Vector indexing and reindexing router (Qdrant)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_active_user
from config import QDRANT_COLLECTION_JOBS, USE_QDRANT_MATCHING
from database.models import Job, User
from database.postgres import get_db
from vector.embedder import get_embedder
from vector.qdrant_client import ensure_collections, upsert_points


router = APIRouter(prefix="/api/v1/vector", tags=["Vector"])


@router.post("/reindex/jobs")
async def reindex_jobs(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Reindex all jobs into Qdrant.

    Admin-only endpoint, used for initial backfill or maintenance.
    """
    if not USE_QDRANT_MATCHING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Qdrant matching is disabled. Enable USE_QDRANT_MATCHING to use this endpoint.",
        )

    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can trigger reindexing.",
        )

    jobs = db.query(Job).all()
    if not jobs:
        return {"indexed": 0}

    embedder = get_embedder()
    ensure_collections(embedder.dimension)

    ids = []
    vectors = []
    payloads = []

    for job in jobs:
        requirements = job.requirements_json or {}
        required_skills = requirements.get("required_skills") or []
        job_description = requirements.get("job_description") or ""

        text_parts = [
            job.title or "",
            job.company or "",
            job.description or "",
            job_description or "",
            ", ".join(required_skills),
        ]
        full_text = " ".join(part for part in text_parts if part)
        if not full_text:
            continue

        vec = embedder.embed_text(full_text)
        ids.append(str(job.id))
        vectors.append(vec)
        payloads.append(
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "salary": job.salary,
                "required_skills": required_skills,
                "created_at": job.created_at.isoformat() if job.created_at else None,
            }
        )

    if ids:
        upsert_points(
            collection=QDRANT_COLLECTION_JOBS,
            ids=ids,
            vectors=vectors,
            payloads=payloads,
        )

    return {"indexed": len(ids)}

