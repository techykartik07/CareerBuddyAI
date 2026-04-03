"""
ai.py — Placeholder router for M2 (Samarth's AI routes)

Samarth: register your AI/LLM endpoints here.
Example routes to add:
  POST /ai/match-jobs     → match resume skills to job descriptions
  POST /ai/suggest        → AI-generated career suggestions
  POST /ai/interview-prep → generate interview questions
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def ai_status():
    """Health check for the AI module."""
    return {"status": "AI module ready", "module": "M2 - Samarth"}


# ── Add your routes below ──────────────────────────────────────────────────

# @router.post("/match-jobs")
# async def match_jobs(payload: dict):
#     ...
