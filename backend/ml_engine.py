import os
from dotenv import load_dotenv
from skills_list import extract_skills

load_dotenv()

# Example mock loading for phase 3, we enclose them in try-except so it doesn't crash phase 2
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    model = None

try:
    from groq import Groq
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        client = Groq(api_key=groq_api_key)
    else:
        client = None
except Exception:
    client = None

def calculate_ats_score(resume_text: str, jd_text: str):
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))
    
    if not jd_skills:
        return {"ats_score": 100, "matched_keywords": list(resume_skills), "missing_keywords": []}
        
    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills.difference(resume_skills)
    
    score = int((len(matched) / len(jd_skills)) * 100)
    
    word_count = len(resume_text.split())
    if word_count < 100:
        score = max(0, score - 20)
        
    return {
        "ats_score": score,
        "matched_keywords": list(matched),
        "missing_keywords": list(missing)
    }

def calculate_job_match(resume_text: str, jd_text: str):
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))
    
    if not jd_skills:
        return {"match_percentage": 100.0, "verdict": "Perfect Match (No requirements provided)"}
        
    matched = resume_skills.intersection(jd_skills)
    percent = (len(matched) / len(jd_skills)) * 100.0
    
    if percent >= 80:
        verdict = "Strong Match"
    elif percent >= 50:
        verdict = "Moderate Match - improve resume"
    else:
        verdict = "Weak Match - significant upskilling required"
        
    return {"match_percentage": round(percent, 1), "verdict": verdict}

def get_skill_gap(resume_skills: list, jd_skills: list):
    res_set = set(resume_skills)
    jd_set = set(jd_skills)
    return {
        "missing_skills": list(jd_set.difference(res_set)),
        "present_skills": list(res_set.intersection(jd_set))
    }

def generate_roadmap(resume_text: str, jd_text: str, missing_skills: list):
    if not missing_skills:
        return "Your profile is an excellent match! No specific upskilling required for this role. Prepare for behavioral interviews."
        
    roadmap = "🚀 Suggested Action Plan:\n\n"
    for i, skill in enumerate(missing_skills[:4]):
        roadmap += f"Week {i+1}: Master {skill.title()} fundamentals.\n"
        roadmap += f"  - Complete an introductory crash course on {skill.title()}.\n"
        roadmap += f"  - Build a small personal project utilizing {skill.title()}.\n\n"
        
    if len(missing_skills) > 4:
        roadmap += f"Future Goals: Consider looking into {', '.join(missing_skills[4:])}.\n"
        
    return roadmap.strip()

def chat_with_assistant(message: str, context: dict):
    return "I am CareerBuddyAI, your offline assistant. To enable fully dynamic conversational AI, please configure an LLM provider key in your backend .env file."
