import requests

BASE = "http://localhost:8000"

bad_resume = "I am a student looking for work. I know some coding."

good_resume = """
Python engineer with 2 years experience. Built ML models using
TensorFlow, scikit-learn and PyTorch. Deployed FastAPI backends
with Docker containers. Experience with data pipelines, pandas,
numpy, and REST APIs. Used Git, GitHub, agile workflows daily.
"""

jd = "Python ML engineer with TensorFlow, FastAPI, Docker experience needed."

print("=== TEST CASE 1: Bad Resume ===")
r = requests.post(f"{BASE}/ai/analyze", json={
    "resume_text":   bad_resume,
    "jd_text":       jd,
    "resume_skills": ["coding"],
    "jd_skills":     ["python","tensorflow","fastapi","docker"]
})
data = r.json()
print("ATS Score:      ", data["ats"]["ats_score"])
print("Job Match:      ", data["match"]["match_percentage"])
print("Missing Skills: ", data["skill_gap"]["missing_skills"])
print("Predicted Role: ", data["role_prediction"]["predicted_role"])

print("\n=== TEST CASE 2: Good Resume ===")
r = requests.post(f"{BASE}/ai/analyze", json={
    "resume_text":   good_resume,
    "jd_text":       jd,
    "resume_skills": ["python","tensorflow","fastapi","docker","pandas","numpy","git"],
    "jd_skills":     ["python","tensorflow","fastapi","docker"]
})
data = r.json()
print("ATS Score:      ", data["ats"]["ats_score"])
print("Job Match:      ", data["match"]["match_percentage"])
print("Missing Skills: ", data["skill_gap"]["missing_skills"])
print("Predicted Role: ", data["role_prediction"]["predicted_role"])