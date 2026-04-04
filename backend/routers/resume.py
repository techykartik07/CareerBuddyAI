"""
resume.py — PDF upload + parsing endpoints

Routes:
  POST /resume/upload    → upload PDF, returns parsed resume data
  POST /resume/parse     → stub endpoint (M2/M3 can code against this immediately)
  GET  /resume/skills    → returns the full skill vocabulary
  GET  /resume/health    → health check
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from parsers.pdf_parser import extract_text_from_pdf
from parsers.contact_parser import extract_contact_info
from skills_list import extract_skills, extract_sections, TECH_SKILLS
import spacy

_nlp = None

def _load_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy model 'en_core_web_sm' not found. "
                "Ensure it's in requirements.txt (as a URL or pip package)."
            )
    return _nlp

router = APIRouter(prefix="/resume", tags=["Resume"])

def extract_orgs(text: str) -> list[str]:
    """Use spaCy NER to extract organisation names."""
    nlp = _load_nlp()
    doc = nlp(text[:5000])  # cap to avoid slow processing
    return list({ent.text for ent in doc.ents if ent.label_ == "ORG"})


@router.get("/health")
def health_check():
    """Health check for the resume module."""
    return {"status": "ok", "module": "resume"}


@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    jd_text: str = Form(default="")
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")
        
    try:
        file_bytes = await file.read()
        if len(file_bytes) == 0:
            raise HTTPException(400, "Empty file uploaded")
        if len(file_bytes) > 5 * 1024 * 1024:    # 5 MB limit
            raise HTTPException(413, "File too large. Max 5MB.")
        text       = extract_text_from_pdf(file_bytes)
        contact    = extract_contact_info(text)
        skills     = extract_skills(text)
        sections   = extract_sections(text)
        return {
            "text":       text,
            "contact":    contact,
            "skills":     skills,
            "education":  sections["education"],
            "experience": sections["experience"],
            "projects":   sections["projects"],
            "word_count": len(text.split()),
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"PDF parsing failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a PDF resume and receive full parsed resume data."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    try:
        file_bytes = await file.read()
        if len(file_bytes) == 0:
            raise HTTPException(400, "Empty file uploaded")
        if len(file_bytes) > 5 * 1024 * 1024:    # 5 MB limit
            raise HTTPException(413, "File too large. Max 5MB.")
        text = extract_text_from_pdf(file_bytes)
        contact = extract_contact_info(text)
        skills = extract_skills(text)
        orgs = extract_orgs(text)

        return {
            "filename": file.filename,
            "contact": contact,
            "skills_matched": skills,
            "organisations": orgs,
            "raw_text_preview": text[:500],
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"PDF parsing failed: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/skills")
def get_skills():
    """Return the full hardcoded skill vocabulary."""
    return {"total": len(TECH_SKILLS), "skills": TECH_SKILLS}

@router.post("/analyze")
async def full_analyze(
    file: UploadFile = File(...),
    jd_text: str = Form(default="")
):
    """Full pipeline: PDF -> parse -> ML scoring -> return all results"""
    from ml_engine import (calculate_ats_score, calculate_job_match,
                           get_skill_gap, generate_roadmap)

    try:
        # Step 1: Parse PDF
        file_bytes = await file.read()
        if len(file_bytes) == 0:
            raise HTTPException(400, "Empty file uploaded")
        if len(file_bytes) > 5 * 1024 * 1024:    # 5 MB limit
            raise HTTPException(413, "File too large. Max 5MB.")
            
        text       = extract_text_from_pdf(file_bytes)
        contact    = extract_contact_info(text)
        resume_skills = extract_skills(text)

        # Step 2: Extract JD skills (simple keyword match from JD text)
        jd_skills  = extract_skills(jd_text) if jd_text else []

        # Step 3: Run ML scoring
        ats   = calculate_ats_score(text, jd_text)
        match = calculate_job_match(text, jd_text)
        gap   = get_skill_gap(resume_skills, jd_skills)
        road  = generate_roadmap(text, jd_text, gap["missing_skills"])

        return {
            "contact":       contact,
            "resume_skills": resume_skills,
            "ats":           ats,
            "match":         match,
            "skill_gap":     gap,
            "roadmap":       road,
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(422, f"PDF parsing failed: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Unexpected error: {str(e)}")

class JDRequest(BaseModel):
    jd_text: str

@router.post("/jd-skills")
def extract_jd_skills(req: JDRequest):
    skills = extract_skills(req.jd_text)
    # Also extract skills not in our list using simple noun phrases
    import re
    extra = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', req.jd_text)
    return {
        "jd_skills": skills,
        "raw_requirements": extra[:15]
    }

SAMPLE_RESULT = {
    "contact": {"name": "Demo Candidate", "email": "demo@example.com"},
    "resume_skills": ["python", "machine learning", "git", "numpy"],
    "ats": {"ats_score": 45, "matched_keywords": ["python"], "missing_keywords": ["fastapi", "docker", "tensorflow"]},
    "match": {"match_percentage": 52.3, "verdict": "Moderate match - improve resume"},
    "skill_gap": {"missing_skills": ["fastapi", "docker", "tensorflow"], "present_skills": ["python", "machine learning"]},
    "roadmap": "Week 1: Learn FastAPI basics...\nWeek 2: Docker fundamentals..."
}

@router.get("/sample")
def get_sample():
    return SAMPLE_RESULT
