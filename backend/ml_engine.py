from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq
import os, re as _re, json as _json, numpy as np, pickle
from dotenv import load_dotenv

load_dotenv()

_groq_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=_groq_key) if _groq_key else None

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

# ── HELPERS ───────────────────────────────────────────────
def _keyword_in_text(keyword: str, text_lower: str) -> bool:
    """Whole-word / whole-phrase match using regex word boundaries.
    Prevents 'data' matching inside 'data structures'."""
    pattern = r'(?<![\w-])' + _re.escape(keyword) + r'(?![\w-])'
    return bool(_re.search(pattern, text_lower))

def _extract_jd_keywords_via_groq(jd_text: str) -> list:
    """Use Groq LLM to extract only real, meaningful keywords from the JD."""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a technical recruiter expert. "
                        "Extract ONLY the specific, concrete skills, tools, technologies, "
                        "frameworks, programming languages, certifications, and domain knowledge "
                        "that a candidate MUST or SHOULD have based on the job description. "
                        "Rules:\n"
                        "- Return ONLY a JSON array of strings, nothing else.\n"
                        "- Each item must be a real skill/tool/technology "
                        "  (e.g. 'python', 'docker', 'rest api', 'data science').\n"
                        "- Do NOT include soft skills like 'communication', 'teamwork', 'ability to work'.\n"
                        "- Do NOT include generic phrases like 'work independently', 'fast learner'.\n"
                        "- Do NOT include company names, locations, or benefits.\n"
                        "- Normalise to lowercase. Max 25 items.\n"
                        'Example output: ["python", "docker", "rest api", "data science", "postgresql"]'
                    )
                },
                {
                    "role": "user",
                    "content": f"Extract skills from this job description:\n\n{jd_text[:3000]}"
                }
            ],
            max_tokens=300,
            temperature=0.1,
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown code fences if the model wraps output in them
        raw = _re.sub(r'^```[\w]*\n?', '', raw).strip('`').strip()
        keywords = _json.loads(raw)
        if isinstance(keywords, list):
            return [str(k).lower().strip() for k in keywords if k and isinstance(k, str)]
        return []
    except Exception:
        return []

# ── 1. ATS SCORE ──────────────────────────────────────────
def calculate_ats_score(resume_text: str, jd_text: str) -> dict:
    try:
        if not resume_text.strip() or not jd_text.strip():
            return {"ats_score": 0, "matched_keywords": [],
                    "missing_keywords": [], "total_keywords_checked": 0}

        # Use Groq to extract only real, relevant JD keywords
        jd_keywords = _extract_jd_keywords_via_groq(jd_text)

        # Fallback: if Groq fails or returns nothing, match against known TECH_SKILLS
        if not jd_keywords:
            jd_lower = jd_text.lower()
            jd_keywords = [s for s in TECH_SKILLS if _keyword_in_text(s, jd_lower)]

        resume_lower = resume_text.lower()
        matched = [k for k in jd_keywords if _keyword_in_text(k, resume_lower)]
        missing = [k for k in jd_keywords if not _keyword_in_text(k, resume_lower)]
        ats_score = int(len(matched) / len(jd_keywords) * 100) if jd_keywords else 0

        return {
            "ats_score":              ats_score,
            "matched_keywords":       matched,
            "missing_keywords":       missing[:15],
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

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        match_pct = round(float(similarity) * 100, 1)

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
            "gap_count":      len(missing),
            "total_jd_skills": len(jd_norm),
        }
    except Exception as e:
        return {"present_skills": [], "missing_skills": [],
                "bonus_skills": [], "gap_count": 0, "error": str(e)}

# ── 4. CAREER ROADMAP via GROQ ────────────────────────────
def generate_roadmap(resume_text: str, jd_text: str, skill_gap: list) -> str:
    if client is None:
        return "Roadmap unavailable: GROQ_API_KEY not configured."
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
        return "Chat unavailable: GROQ_API_KEY not configured."
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