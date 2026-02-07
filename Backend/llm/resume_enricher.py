from typing import Any, Dict, List

from config import GROQ_API_KEY
from llm.groq_client import get_groq_client


def _build_enrichment_prompt(parsed_data: Dict[str, Any]) -> str:
    """
    Build a compact prompt from parsed resume data.

    We only send the most relevant fields to keep token usage under control.
    """
    raw_text = parsed_data.get("raw_text", "")
    name = parsed_data.get("name") or ""
    skills = parsed_data.get("skills") or []
    experience = parsed_data.get("experience") or []
    education = parsed_data.get("education") or []

    snippet = raw_text[:4000]  # hard cap to keep prompts bounded

    return (
        "You are an expert career coach and resume analyst. "
        "Given the parsed resume data and raw text, produce a concise JSON summary "
        "that normalizes skills and infers key metadata.\n\n"
        "Requirements:\n"
        "- Respond with ONLY a JSON object, no extra text.\n"
        "- Fields:\n"
        "  - normalized_skills: list[str] of deduplicated, canonical skill names.\n"
        "  - inferred_role: short string (e.g., 'Backend Developer', 'Data Analyst').\n"
        "  - seniority: one of ['intern', 'junior', 'mid', 'senior', 'lead', 'unknown'].\n"
        "  - summary: 2-3 sentence plain-text summary of the candidate profile.\n"
        "  - strengths: list[str] of 3-6 bullet-style strengths.\n"
        "  - weaknesses: list[str] of 3-6 improvement areas (resume or profile).\n"
        "  - recommended_keywords: list[str] of 5-15 keywords to help ATS for tech roles.\n\n"
        f"Name: {name}\n"
        f"Existing parsed skills: {skills}\n"
        f"Parsed experience entries: {experience[:3]}\n"
        f"Parsed education entries: {education[:3]}\n\n"
        f"Raw resume text (may be truncated):\n{snippet}\n"
    )


def enrich_resume(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use Groq to enrich parsed resume data with normalized skills and meta information.

    If GROQ is not configured or any error occurs, this function returns an empty dict.
    """
    if not GROQ_API_KEY:
        return {}

    try:
        client = get_groq_client()
        system_prompt = (
            "You turn parsed resume data into a clean, compact JSON summary for an ATS system. "
            "Always return valid JSON only."
        )
        user_prompt = _build_enrichment_prompt(parsed_data)
        result = client.chat_json(system_prompt=system_prompt, user_prompt=user_prompt)

        # Ensure expected keys exist
        enriched: Dict[str, Any] = {
            "normalized_skills": result.get("normalized_skills", []),
            "inferred_role": result.get("inferred_role", "unknown"),
            "seniority": result.get("seniority", "unknown"),
            "summary": result.get("summary", ""),
            "strengths": result.get("strengths", []),
            "weaknesses": result.get("weaknesses", []),
            "recommended_keywords": result.get("recommended_keywords", []),
        }
        return enriched
    except Exception as e:
        # Enrichment is optional; swallow errors and proceed without it
        print(f"[LLM] Resume enrichment failed: {e}")
        return {}

