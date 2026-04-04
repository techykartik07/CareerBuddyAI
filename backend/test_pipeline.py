import os
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(current_dir, "sample_resume.pdf")

with open(pdf_path, "rb") as f:
    resp = requests.post(
        "http://localhost:8000/resume/analyze",
        files={"file": ("resume.pdf", f, "application/pdf")},
        data={"jd_text": "Python developer with ML experience, FastAPI, Docker"}
    )
    
data = resp.json()
print("Name:", data["contact"]["name"])
print("Email:", data["contact"]["email"])
print("Skills found:", data["resume_skills"])
print("ATS Score:", data["ats"]["ats_score"])
print("Job Match:", data["match"]["match_percentage"])
