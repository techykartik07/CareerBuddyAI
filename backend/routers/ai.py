from fastapi import APIRouter
from pydantic import BaseModel
from ml_engine import (calculate_ats_score, calculate_job_match,
                       get_skill_gap, generate_roadmap, chat_with_assistant)

router = APIRouter(prefix="/ai", tags=["AI/ML"])

class AnalyzeRequest(BaseModel):
    resume_text: str
    jd_text: str
    resume_skills: list = []
    jd_skills: list = []

class ChatRequest(BaseModel):
    message: str
    context: dict = {}

@router.post("/ats-score")
def ats_score(req: AnalyzeRequest):
    return calculate_ats_score(req.resume_text, req.jd_text)

@router.post("/job-match")
def job_match(req: AnalyzeRequest):
    return calculate_job_match(req.resume_text, req.jd_text)

@router.post("/skill-gap")
def skill_gap(req: AnalyzeRequest):
    return get_skill_gap(req.resume_skills, req.jd_skills)

@router.post("/roadmap")
def roadmap(req: AnalyzeRequest):
    gap = get_skill_gap(req.resume_skills, req.jd_skills)
    text = generate_roadmap(req.resume_text, req.jd_text, gap.get("missing_skills", []))
    return {"roadmap": text}

@router.post("/chat")
def chat(req: ChatRequest):
    reply = chat_with_assistant(req.message, req.context)
    return {"reply": reply}
