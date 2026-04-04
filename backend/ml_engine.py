from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq
import os, numpy as np, pickle
from dotenv import load_dotenv

load_dotenv()

<<<<<<< HEAD
_groq_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=_groq_key) if _groq_key else None
=======
_model = None
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
>>>>>>> ff7001643c2aa5173e5264c71a91bc2b1dd73df5

def _load_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

# ── SKILL VOCABULARY ──────────────────────────────────────
TECH_SKILLS = [
    "python","java","javascript","typescript","c++","c","go","rust",
    "kotlin","swift","r","scala","sql","html","css","php","ruby",
    "machine learning","deep learning","tensorflow","pytorch","keras",
    "scikit-learn","nlp","computer vision","transformers","bert",
    "pandas","numpy","matplotlib","data analysis","data science",
    "power bi","tableau","excel","spark","hadoop","hive",
    "fastapi","django","flask","node.js","react","vue","angular",
    "rest api","graphql","docker","kubernetes","aws","azure","gcp",
    "git","github","linux","bash","postman","jira","agile","scrum",
    "mongodb","postgresql","mysql","redis","elasticsearch",
    "blockchain","solidity","devops","ci/cd","jenkins",
]

SKILL_ALIASES = {
    "ml":"machine learning","ai":"artificial intelligence",
    "js":"javascript","ts":"typescript","ds":"data science",
    "dl":"deep learning","k8s":"kubernetes","tf":"tensorflow",
}

# ── 1. ATS SCORE ──────────────────────────────────────────
def calculate_ats_score(resume_text: str, jd_text: str) -> dict:
    try:
        if not resume_text.strip() or not jd_text.strip():
            return {"ats_score": 0, "matched_keywords": [],
                    "missing_keywords": [], "total_keywords_checked": 0}

        vectorizer = TfidfVectorizer(
            stop_words="english", max_features=30, ngram_range=(1,2)
        )
        vectorizer.fit([jd_text])
        jd_keywords = vectorizer.get_feature_names_out().tolist()

        resume_lower = resume_text.lower()
        matched = [k for k in jd_keywords if k in resume_lower]
        missing = [k for k in jd_keywords if k not in resume_lower]
        ats_score = int(len(matched) / len(jd_keywords) * 100) if jd_keywords else 0

        return {
            "ats_score":              ats_score,
            "matched_keywords":       matched,
            "missing_keywords":       missing[:10],
            "total_keywords_checked": len(jd_keywords)
        }
    except Exception as e:
        return {"ats_score": 0, "matched_keywords": [],
                "missing_keywords": [], "error": str(e)}

# ── 2. JOB MATCH % ────────────────────────────────────────
def calculate_job_match(resume_text: str, jd_text: str) -> dict:
    try:
        if not resume_text.strip() or not jd_text.strip():
            return {"match_percentage": 0.0, "verdict": "Insufficient text"}

        model = _load_model()
        embeddings  = model.encode([resume_text, jd_text])
        similarity  = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        match_pct   = round(float(similarity) * 100, 1)

        if match_pct >= 75:
            verdict = "Strong match"
        elif match_pct >= 50:
            verdict = "Moderate match — improve your resume"
        else:
            verdict = "Weak match — consider a different role"

        return {"match_percentage": match_pct, "verdict": verdict}
    except Exception as e:
        return {"match_percentage": 0.0, "verdict": "Error", "error": str(e)}

# ── 3. SKILL GAP ──────────────────────────────────────────
def normalize_skill(skill: str) -> str:
    s = skill.lower().strip()
    return SKILL_ALIASES.get(s, s)

def get_skill_gap(resume_skills: list, jd_skills: list) -> dict:
    try:
        resume_norm = set(normalize_skill(s) for s in resume_skills)
        jd_norm     = set(normalize_skill(s) for s in jd_skills)

        present = sorted(resume_norm & jd_norm)
        missing = sorted(jd_norm - resume_norm)
        bonus   = sorted(resume_norm - jd_norm)

        return {
            "present_skills": present,
            "missing_skills": missing,
            "bonus_skills":   bonus,
            "gap_count":      len(missing)
        }
    except Exception as e:
        return {"present_skills": [], "missing_skills": [],
                "bonus_skills": [], "gap_count": 0, "error": str(e)}

# ── 4. CAREER ROADMAP via GROQ ────────────────────────────
def generate_roadmap(resume_text: str, jd_text: str, skill_gap: list) -> str:
    if client is None:
        return "AI features unavailable: GROQ_API_KEY not configured"
    try:
        missing_str = ", ".join(skill_gap) if skill_gap else "None identified"

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert career coach.
Here is the candidate's resume:
---
{resume_text[:2000]}
---
Target job description:
---
{jd_text[:1000]}
---
Skills they are missing: {missing_str}

Generate a personalised 4-week career roadmap.
For each week specify:
- What to learn (specific skill/topic)
- One free resource (course or website name)
- One mini project to build
Keep it concise, practical and encouraging.
Maximum 300 words."""
                },
                {
                    "role": "user",
                    "content": "Generate my personalised 4-week career roadmap."
                }
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Roadmap generation failed: {str(e)}"

# ── 5. AI CHATBOT via GROQ ────────────────────────────────
def chat_with_assistant(user_message: str, context: dict) -> str:
    if client is None:
        return "AI features unavailable: GROQ_API_KEY not configured"
    try:
        resume_text    = context.get("resume_text", "Not provided")
        jd_text        = context.get("jd_text", "Not provided")
        ats_score      = context.get("ats_score", "Not calculated")
        match_pct      = context.get("match_percentage", "Not calculated")
        missing_skills = context.get("missing_skills", [])

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are CareerBuddy AI, a friendly career assistant.
You have full context about this user:
Resume: {resume_text[:800]}
Target job: {jd_text[:500]}
ATS score: {ats_score}%
Job match: {match_pct}%
Missing skills: {', '.join(missing_skills) if missing_skills else 'None'}

Answer their career questions using this context.
Be specific, practical and encouraging.
Maximum 3 sentences unless more detail is requested."""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Assistant error: {str(e)}"

# ── 6. JOB ROLE CLASSIFIER ────────────────────────────────
_classifier = None
_tfidf      = None
_categories = None

def _load_classifier():
    global _classifier, _tfidf, _categories
    if _classifier is not None:
        return
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    clf_path   = os.path.join(models_dir, "job_classifier.pkl")
    vec_path   = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    cat_path   = os.path.join(models_dir, "categories.pkl")
    if not os.path.exists(clf_path):
        raise FileNotFoundError("Run train_classifier.py first.")
    with open(clf_path, "rb") as f: _classifier = pickle.load(f)
    with open(vec_path, "rb") as f: _tfidf      = pickle.load(f)
    with open(cat_path, "rb") as f: _categories = pickle.load(f)

def predict_job_role(resume_text: str) -> dict:
    if not resume_text or not resume_text.strip():
        return {"predicted_role": "Unknown", "confidence": 0.0,
                "top_3_matches": [], "total_categories": 0,
                "error": "Empty resume text"}
    try:
        _load_classifier()
        vec            = _tfidf.transform([resume_text])
        predicted_role = _classifier.predict(vec)[0]
        probs          = _classifier.predict_proba(vec)[0]
        all_scores     = sorted(zip(_classifier.classes_, probs),
                                key=lambda x: x[1], reverse=True)
        top_3 = [{"role": r, "confidence": round(float(p)*100, 1)}
                 for r, p in all_scores[:3]]
        return {
            "predicted_role":   predicted_role,
            "confidence":       top_3[0]["confidence"],
            "top_3_matches":    top_3,
            "total_categories": len(_classifier.classes_)
        }
    except FileNotFoundError as e:
        return {"predicted_role": "Model not trained", "confidence": 0.0,
                "top_3_matches": [], "error": str(e)}
    except Exception as e:
        return {"predicted_role": "Error", "confidence": 0.0,
                "top_3_matches": [], "error": str(e)}