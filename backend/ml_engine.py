from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq
import os, numpy as np
from dotenv import load_dotenv
import pickle
import os

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

# Load trained classifier (loaded once at startup, reused for every request)
_classifier  = None
_tfidf       = None
_categories  = None

def _load_classifier():
    """Lazy-load the classifier on first use."""
    global _classifier, _tfidf, _categories
    if _classifier is not None:
        return  # already loaded

    models_dir = os.path.join(os.path.dirname(__file__), "models")
    clf_path   = os.path.join(models_dir, "job_classifier.pkl")
    vec_path   = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    cat_path   = os.path.join(models_dir, "categories.pkl")

    if not os.path.exists(clf_path):
        raise FileNotFoundError(
            "Trained model not found. Run train_classifier.py first."
        )

    with open(clf_path, "rb") as f: _classifier = pickle.load(f)
    with open(vec_path, "rb") as f: _tfidf      = pickle.load(f)
    with open(cat_path, "rb") as f: _categories = pickle.load(f)
def predict_job_role(resume_text: str) -> dict:
    """
    Predicts the most suitable job role for a given resume.
    Uses a Logistic Regression model trained on 2,400 labelled resumes.

    Returns:
        predicted_role    : The top predicted job category
        confidence        : Confidence % for the top prediction
        top_3_matches     : Top 3 roles with confidence scores
        total_categories  : How many job categories the model knows
    """
    if not resume_text or not resume_text.strip():
        return {
            "predicted_role":   "Unknown",
            "confidence":        0.0,
            "top_3_matches":    [],
            "total_categories":  0,
            "error": "Empty resume text provided"
        }

    try:
        _load_classifier()  # loads model if not already loaded

        # Vectorize the resume text using the same TF-IDF as training
        vec   = _tfidf.transform([resume_text])

        # Get predicted role
        predicted_role = _classifier.predict(vec)[0]

        # Get probability scores for ALL categories
        probs = _classifier.predict_proba(vec)[0]

        # Build top 3 matches sorted by confidence
        all_scores = sorted(
            zip(_classifier.classes_, probs),
            key=lambda x: x[1],
            reverse=True
        )
        top_3 = [
            {
                "role":       role,
                "confidence": round(float(prob) * 100, 1)
            }
            for role, prob in all_scores[:3]
        ]

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