def calculate_ats_score(resume_text: str, jd_text: str):
    return {"score": 85, "message": "Dummy ATS score"}

def calculate_job_match(resume_text: str, jd_text: str):
    return {"match": 90, "message": "Dummy job match"}

def get_skill_gap(resume_skills: list, jd_skills: list):
    return {"missing_skills": ["Dummy Skill 1", "Dummy Skill 2"]}

def generate_roadmap(resume_text: str, jd_text: str, missing_skills: list):
    return "Dummy roadmap based on missing skills"

def chat_with_assistant(message: str, context: dict):
    return "Dummy reply from assistant"
