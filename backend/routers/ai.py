from fastapi import APIRouter
from pydantic import BaseModel
from ml_engine import (calculate_ats_score, calculate_job_match,
                        get_skill_gap, generate_roadmap, chat_with_assistant,
                        predict_job_role)
from parsers.contact_parser import extract_contact_info

router = APIRouter(prefix="/ai", tags=["AI/ML"])

class AnalyzeRequest(BaseModel):
    resume_text: str
    jd_text: str
    resume_skills: list = []
    jd_skills: list = []

class RoleRequest(BaseModel):
    resume_text: str

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

@router.post("/predict-role")
def predict_role(req: RoleRequest):
    """
    Predicts the best-fit job role for a given resume.

    Uses a Logistic Regression model trained on 2,400 labelled
    resumes from Kaggle across 24 job categories.
    Accuracy: ~85-92% on held-out test set.
    """
    if not req.resume_text or not req.resume_text.strip():
        return {
            "predicted_role":  "Unknown",
            "confidence":       0.0,
            "top_3_matches":   [],
            "message": "Please provide resume text."
        }

    result = predict_job_role(req.resume_text)
    return result

@router.post("/analyze")
def full_analyze(req: AnalyzeRequest):
    text = req.resume_text
    jd_text = req.jd_text
    resume_skills = req.resume_skills
    jd_skills = req.jd_skills

    contact = extract_contact_info(text)
    ats = calculate_ats_score(text, jd_text)
    match = calculate_job_match(text, jd_text)
    gap = get_skill_gap(resume_skills, jd_skills)
    road  = generate_roadmap(text, jd_text, gap.get("missing_skills", []))
    role  = predict_job_role(text)

    return {
        "contact":        contact,
        "resume_skills":  resume_skills,
        "ats":            ats,
        "match":          match,
        "skill_gap":      gap,
        "roadmap":        road,
        "role_prediction": role
    }
