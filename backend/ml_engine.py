from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq
import os, numpy as np
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer('all-MiniLM-L6-v2')
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calculate_ats_score(resume_text: str, jd_text: str) -> dict:
    # TODO: build in Phase 2
    return {"ats_score": 70, "matched_keywords": [], "missing_keywords": []}

def calculate_job_match(resume_text: str, jd_text: str) -> dict:
    # TODO: build in Phase 2
    return {"match_percentage": 65.0}

def get_skill_gap(resume_skills: list, jd_skills: list) -> dict:
    # TODO: build in Phase 2
    return {"missing_skills": [], "present_skills": []}

def generate_roadmap(resume_text: str, jd_text: str, skill_gap: list) -> str:
    # TODO: Groq API call in Phase 3
    return "Roadmap will be generated here"

def chat_with_assistant(user_message: str, context: dict) -> str:
    # TODO: Groq API call in Phase 3
    return "AI assistant will respond here"
