# 🎯 CareerBuddyAI

> **Hacksagon 2026 · QUANT 4 · ABV-IIITM · IEEE MP Section**  
> *A National Level Software & Hardware Hackathon*

**CareerBuddy AI** is an AI-powered career guidance platform that analyses resumes using NLP, matches users with suitable job roles, identifies skill gaps, and generates personalised learning roadmaps — powered by a trained ML classifier and Groq's LLaMA 3.1 API.

---

## 🚨 Problem Statement

- Students and fresh graduates face confusion when choosing suitable career paths
- Existing platforms provide generic recommendations, not AI-driven insights
- Resume–job mismatch leads to low employability and high rejection rates
- No personalised guidance based on individual skills and interests

---

## 💡 Proposed Solution

CareerBuddy AI addresses these pain points through a full-stack AI pipeline:

1. **Resume Parsing** — Upload a PDF; NLP extracts skills, education, and experience
2. **ATS Compatibility Analysis** — TF-IDF keyword matching scores your resume against industry hiring systems
3. **Job Description Matching** — Cosine similarity between resume and JD embeddings gives a match percentage
4. **Skill Gap Analysis** — Compares your skills vs. required JD skills and ranks what's missing
5. **Job Role Prediction** — Logistic Regression classifier trained on 166 labelled resumes (82.4% accuracy) predicts your best-fit role
6. **Personalised Career Roadmap** — Groq LLaMA 3.1 generates a week-by-week learning plan based on your specific skill gaps
7. **AI Career Assistant** — Chat with an AI that knows your resume, JD, and roadmap

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)              │
│   Upload Page → Results Dashboard → AI Chat Panel          │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP / REST
┌───────────────────────▼─────────────────────────────────────┐
│                     BACKEND (FastAPI)                       │
│   /resume/parse   /ai/ats-score   /ai/job-match             │
│   /ai/skill-gap   /ai/roadmap     /ai/chat                  │
│   /ai/predict-role               /ai/analyze                │
└──────────┬────────────────────────────┬─────────────────────┘
           │                            │
┌──────────▼──────────┐    ┌────────────▼──────────────────────┐
│  PDF Parser (NLP)   │    │     ML Engine                     │
│  pdfplumber + spaCy │    │  sentence-transformers (embeddings)│
│  regex contact info │    │  scikit-learn (TF-IDF + LR model) │
└─────────────────────┘    │  Groq LLaMA 3.1 API               │
                           └───────────────────────────────────┘
```

### System Flow

```
Resume Upload → Resume Parsing (NLP) → ATS Compatibility Analysis
                                              ↓
                                   Is ATS Score ≥ Threshold?
                                    ├── No  → Show Improvement Tips
                                    └── Yes → Resume–Job Matching
                                                    ↓
                                         Match Score ≥ Required?
                                          ├── No  → Skill Gap Analyzer
                                          └── Yes → Job Role Prediction
                                                          ↓
                                              Personalised Career Roadmap
                                                          ↓
                                              AI Career Assistant Chat
                                                          ↓
                                              Results Dashboard
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, Recharts, React Router |
| Backend | FastAPI, Python 3.11+, Uvicorn |
| PDF Parsing | pdfplumber, spaCy (`en_core_web_sm`) |
| ML — Embeddings | sentence-transformers (`all-MiniLM-L6-v2`), cosine similarity |
| ML — Classifier | scikit-learn Logistic Regression, TF-IDF vectorizer |
| ML — Training Data | Kaggle Resume Dataset (166 unique resumes, 25 categories, 82.4% accuracy) |
| LLM | Groq API (`llama-3.1-8b-instant`) |
| Deployment | Render (backend), Vercel (frontend) |
| Version Control | GitHub |

---

## 🤖 ML Pipeline Details

| Component | Algorithm | Details |
|---|---|---|
| ATS Score | TF-IDF keyword extraction | Extracts top 30 keywords from JD, checks presence in resume |
| Job Match % | Sentence transformer embeddings + cosine similarity | `all-MiniLM-L6-v2`, 384-dimensional vectors |
| Job Role Classifier | Logistic Regression | Trained on 166 unique resumes, 25 categories, **82.4% accuracy** |
| Skill Gap | Set difference on normalised skill lists | 80+ skill vocabulary with alias normalisation |
| Career Roadmap | Groq LLaMA 3.1 | Context-injected with resume + JD + missing skills |
| AI Chatbot | Groq LLaMA 3.1 | Context-injected with full user profile and scores |

> **Data cleaning note:** The source dataset contained 796 duplicate entries (82% duplication rate). We identified and removed all duplicates before training to prevent data leakage. Without this step, accuracy was artificially inflated to 99.5%.

---

## 📁 Project Structure

```
careerbuddy-ai/
├── backend/
│   ├── main.py                  # FastAPI entry point, CORS config
│   ├── ml_engine.py             # ATS scorer, job match, skill gap, Groq calls, classifier
│   ├── train_classifier.py      # Training script — run once to generate .pkl files
│   ├── verify_model.py          # Model verification and test predictions
│   ├── skills_list.py           # Curated skill vocabulary (80+ skills)
│   ├── requirements.txt
│   ├── .env                     # API keys (never commit!)
│   ├── data/
│   │   └── Resume.csv           # Training dataset (not committed — too large)
│   ├── models/
│   │   ├── job_classifier.pkl   # Trained model (not committed — generated locally)
│   │   └── tfidf_vectorizer.pkl # Trained vectorizer (not committed)
│   ├── parsers/
│   │   ├── pdf_parser.py        # pdfplumber text extraction
│   │   └── contact_parser.py    # regex for email, phone, name
│   └── routers/
│       ├── resume.py            # /resume/* endpoints
│       └── ai.py                # /ai/* endpoints
│
└── frontend/
    ├── src/
    │   ├── App.jsx              # React Router setup
    │   ├── pages/
    │   │   ├── UploadPage.jsx   # PDF upload + JD input
    │   │   └── ResultsPage.jsx  # Dashboard with all scores
    │   ├── components/
    │   │   ├── DropZone.jsx     # Drag-and-drop file upload
    │   │   ├── ScoreGauge.jsx   # Radial chart for ATS / Job Match %
    │   │   ├── SkillGapList.jsx # Missing skills display
    │   │   ├── RoadmapPanel.jsx # Career roadmap markdown renderer
    │   │   └── ChatPanel.jsx    # AI chatbot interface
    │   └── api/
    │       └── client.js        # All Axios API calls in one place
    └── .env                     # VITE_API_URL (never commit!)
```

---

## ✨ Features

- 🤖 **AI Resume Parsing** — NLP-powered extraction of skills, education, and experience from PDF
- 📊 **ATS Score** — TF-IDF keyword matching to align with industry hiring systems
- 🎯 **Job Match %** — Semantic similarity between resume and job description using sentence transformers
- 🔍 **Skill Gap Analysis** — Ranked list of missing skills with learning priorities
- 🏷️ **Job Role Prediction** — ML classifier predicts your best-fit role with confidence scores
- 🗺️ **Career Roadmap** — Groq LLaMA 3.1 generated week-by-week learning plan based on your skill gaps
- 💬 **AI Career Assistant** — Context-aware chatbot using your resume, JD, scores, and roadmap
- 📈 **Results Dashboard** — All insights in one clean, visual interface

---

## ⚙️ API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Server health check |
| `POST` | `/resume/parse` | Upload PDF, returns structured resume data |
| `POST` | `/ai/ats-score` | Calculate ATS compatibility score |
| `POST` | `/ai/job-match` | Calculate resume–JD similarity percentage |
| `POST` | `/ai/skill-gap` | Identify missing skills vs. JD requirements |
| `POST` | `/ai/predict-role` | Predict best-fit job role using trained ML classifier |
| `POST` | `/ai/roadmap` | Generate personalised learning roadmap via Groq LLaMA 3.1 |
| `POST` | `/ai/chat` | Chat with AI career assistant |
| `POST` | `/ai/analyze` | Combined endpoint — returns all results in one call |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Groq API key](https://console.groq.com) (free)

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/techykartik07/CareerBuddyAI.git
cd CareerBuddyAI/backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Pre-download sentence-transformers model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2'); print('Model ready!')"

# Create .env file and add your Groq API key
echo "GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx" > .env

# Train the job role classifier (requires data/Resume.csv)
python train_classifier.py

# Start the server
uvicorn main:app --reload --port 8000
```

Backend live at: `https://careerbuddyai-backend-kartik.onrender.com`  
API docs at: `https://careerbuddyai-backend-kartik.onrender.com/docs`

### Frontend Setup

```bash
cd CareerBuddyAI/frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=https://careerbuddyai-backend-kartik.onrender.com" > .env

# Start dev server
npm run dev
```

Frontend live at: `https://career-buddy-ai-kappa.vercel.app`

---

## 🌐 Deployment

| Service | Platform | Configuration |
|---|---|---|
| Backend | [Render](https://render.com) | Root: `backend/`, Build: `pip install -r requirements.txt && python -m spacy download en_core_web_sm && python train_classifier.py`, Start: `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Frontend | [Vercel](https://vercel.com) | Root: `frontend/`, Framework: Vite, Env: `VITE_API_URL=https://careerbuddyai-backend-kartik.onrender.com` |

**Environment variables to add on Render:**
- `GROQ_API_KEY` — your Groq API key from console.groq.com

---

## ⚠️ Known Limitations

- **Limited training data** — Classifier trained on 166 unique resumes; confidence scores improve with more data
- **Bias in job-market data** — Regular model evaluation and fairness checks are required
- **Resume quality dependency** — Scanned or image-based PDFs cannot be parsed (text layer required)
- **Dynamic job market** — Skill recommendations may lag behind rapidly evolving roles
- **Internet & compute dependency** — Groq API and sentence-transformers require connectivity

---

## 👥 Team — QUANT 4

| Member | Role | Responsibility |
|---|---|---|
| **Samarth Sharma** | AI/ML Engineer | ML classifier training, ATS scoring, job matching, skill gap, Groq API |
| **Ajay Kumar** | Backend Lead | FastAPI server, PDF parsing, NLP extraction, API endpoints |
| **Kaustubh Mishra** | Frontend Lead | React UI, dashboard, score visualisation, AI chat interface |
| **Kartik Khemani** | DevOps & Integration | GitHub, Render deployment, Vercel, CORS & integration |

---

## 📄 License

This project was built for **Hacksagon 2026** at ABV-IIITM. All rights reserved by QUANT 4.