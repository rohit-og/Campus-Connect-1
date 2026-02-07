from typing import Any, Dict, Tuple

from config import GROQ_API_KEY
from llm.groq_client import get_groq_client


def classify_hr_intent(message: str) -> Tuple[str, Dict[str, Any]]:
    """
    Use Groq to classify HR/admin chat messages into structured intents.

    Returns (intent, params). Falls back to ("help", {}) on failure.
    """
    if not GROQ_API_KEY:
        return "help", {}

    system_prompt = (
        "You are an intent classifier for an HR recruitment assistant. "
        "Given a natural language message, map it to ONE of these intents and parameters:\n\n"
        "Intents:\n"
        "- list_jobs: list jobs, optional company filter.\n"
        "- get_job: show details for a specific job. params: job_id:int.\n"
        "- list_candidates: list candidates.\n"
        "- get_candidate: show candidate by numeric id. params: candidate_id:int.\n"
        "- get_candidate_by_name: show candidate by name. params: candidate_name:str.\n"
        "- search_candidates_by_skill: candidates with a given skill. params: skill:str.\n"
        "- get_candidate_evaluations: evaluations for a candidate id. params: candidate_id:int.\n"
        "- get_candidate_evaluations_by_name: evaluations for a candidate name. params: candidate_name:str.\n"
        "- get_job_evaluations: evaluations for a job id. params: job_id:int.\n"
        "- get_application_count: application statistics for a job id. params: job_id:int.\n"
        "- get_statistics: overall funnel statistics.\n"
        "- help: when nothing matches clearly.\n\n"
        "Respond with ONLY JSON: {\"intent\": string, \"params\": object}."
    )
    user_prompt = f"Message: {message}"

    try:
        client = get_groq_client()
        result = client.chat_json(system_prompt=system_prompt, user_prompt=user_prompt)
        intent = str(result.get("intent", "help"))
        params = result.get("params") or {}
        if not isinstance(params, dict):
            params = {}
        return intent, params
    except Exception as e:
        print(f"[LLM] HR intent classification failed: {e}")
        return "help", {}


def classify_student_intent(message: str) -> Tuple[str, Dict[str, Any]]:
    """
    Use Groq to classify student chat messages into structured intents.

    Returns (intent, params). Falls back to ("help", {}) on failure.
    """
    if not GROQ_API_KEY:
        return "help", {}

    system_prompt = (
        "You are an intent classifier for a student career assistant. "
        "Given a natural language message, map it to ONE of these intents and parameters:\n\n"
        "Intents:\n"
        "- search_jobs: natural language job search. params: query:str.\n"
        "- get_job_details: job details with match analysis. params: job_id:int.\n"
        "- analyze_skill_gap_for_job: skill gap for a job id. params: job_id:int.\n"
        "- analyze_skill_gap: generic skill gap; use when job id is not clear. params may include job_id:int.\n"
        "- get_my_applications: show student's applications.\n"
        "- get_resume_feedback: resume feedback for a job. params: job_id:int (if present in message).\n"
        "- interpret_rejection: explain rejection for a job. params: job_id:int.\n"
        "- help: when nothing matches clearly.\n\n"
        "Respond with ONLY JSON: {\"intent\": string, \"params\": object}."
    )
    user_prompt = f"Message: {message}"

    try:
        client = get_groq_client()
        result = client.chat_json(system_prompt=system_prompt, user_prompt=user_prompt)
        intent = str(result.get("intent", "help"))
        params = result.get("params") or {}
        if not isinstance(params, dict):
            params = {}
        return intent, params
    except Exception as e:
        print(f"[LLM] Student intent classification failed: {e}")
        return "help", {}

