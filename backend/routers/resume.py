"""
resume.py — PDF upload + parsing endpoints

Routes:
  POST /resume/upload    → upload PDF, returns parsed resume data
  POST /resume/parse     → stub endpoint (M2/M3 can code against this immediately)
  GET  /resume/skills    → returns the full skill vocabulary
  GET  /resume/health    → health check
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from parsers.pdf_parser import extract_text_from_pdf
from parsers.contact_parser import extract_contact_info
from skills_list import SKILLS
import spacy

router = APIRouter()

# Load spaCy model once at startup
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError(
        "spaCy model 'en_core_web_sm' not found. "
        "Run: python -m spacy download en_core_web_sm"
    )


def extract_skills(text: str) -> list[str]:
    """Match skill keywords from SKILLS vocabulary against resume text."""
    text_lower = text.lower()
    return [skill for skill in SKILLS if skill.lower() in text_lower]


def extract_orgs(text: str) -> list[str]:
    """Use spaCy NER to extract organisation names."""
    doc = nlp(text[:5000])  # cap to avoid slow processing
    return list({ent.text for ent in doc.ents if ent.label_ == "ORG"})


@router.get("/health")
def health_check():
    """Health check for the resume module."""
    return {"status": "ok", "module": "resume"}


@router.post("/parse")
async def parse_resume(file: UploadFile = File(...), jd_text: str = ""):
    """
    Parse a resume PDF and return structured data.

    - **file**: PDF resume to upload
    - **jd_text**: (optional) job description text for future matching

    TODO (Phase 2): replace stub values with real NLP extraction.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    file_bytes = await file.read()
    try:
        text = extract_text_from_pdf(file_bytes)
    except ValueError as e:
        # Handle scanned/image PDFs gracefully
        return {"error": "Please upload a text-based PDF", "detail": str(e)}

    contact = extract_contact_info(text)
    skills = extract_skills(text)

    return {
        "text": text[:3000],
        "contact": contact,
        "skills": skills,
        "education": [],    # TODO Phase 2: NLP-based education extraction
        "experience": [],   # TODO Phase 2: NLP-based experience extraction
    }


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a PDF resume and receive full parsed resume data."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    file_bytes = await file.read()
    try:
        text = extract_text_from_pdf(file_bytes)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail="Please upload a text-based PDF",
        )

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


@router.get("/skills")
def get_skills():
    """Return the full hardcoded skill vocabulary."""
    return {"total": len(SKILLS), "skills": SKILLS}
