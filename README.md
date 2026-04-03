# 🎯 CareerBuddyAI

> **Hacksagon 2026 · QUANT 4 · ABV-IIITM · IEEE MP Section**  
> *A National Level Software & Hardware Hackathon*

**CareerBuddy AI** is an AI-powered career guidance platform that analyses resumes using NLP, matches users with suitable job roles, identifies skill gaps, and generates personalised learning roadmaps — all powered by Claude AI.

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
5. **Personalised Career Roadmap** — Claude AI generates a week-by-week learning plan
6. **AI Career Assistant** — Chat with an AI that knows your resume, JD, and roadmap

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
└──────────┬────────────────────────────┬─────────────────────┘
           │                            │
┌──────────▼──────────┐    ┌────────────▼──────────────────┐
│  PDF Parser (NLP)   │    │     ML Engine                 │
│  pdfplumber + spaCy │    │  sentence-transformers        │
│  regex contact info │    │  scikit-learn (TF-IDF)        │
└─────────────────────┘    │  Anthropic Claude API         │
                           └───────────────────────────────┘
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
                                          └── Yes → Personalised Roadmap
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
| AI / ML | sentence-transformers (`all-MiniLM-L6-v2`), scikit-learn (TF-IDF) |
| LLM | Anthropic Claude API (`claude-opus-4-6`) |
| Deployment | Render (backend), Vercel (frontend) |
| Version Control | GitHub |

---

## 📁 Project Structure

```
careerbuddy-ai/
├── backend/
│   ├── main.py                  # FastAPI entry point, CORS config
│   ├── ml_engine.py             # ATS scorer, job match, skill gap, Claude calls
│   ├── skills_list.py           # Curated skill vocabulary
│   ├── requirements.txt
│   ├── .env                     # API keys (never commit!)
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
- 📊 **ATS Score** — Keyword matching to align with industry hiring systems
- 🎯 **Job Match %** — Semantic similarity between resume and job description
- 🔍 **Skill Gap Analysis** — Ranked list of missing skills with learning priorities
- 🗺️ **Career Roadmap** — Claude-generated week/month learning plan with certification suggestions
- 💬 **AI Career Assistant** — Context-aware chatbot using resume + JD + roadmap data
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
| `POST` | `/ai/roadmap` | Generate personalised learning roadmap via Claude |
| `POST` | `/ai/chat` | Chat with AI career assistant |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com)

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/careerbuddy-ai.git
cd careerbuddy-ai/backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Pre-download sentence-transformers model (saves time on first run)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2'); print('Model ready!')"

# Create .env file and add your API key
echo "ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx" > .env

# Start the server
uvicorn main:app --reload --port 8000
```

Backend will be live at `http://localhost:8000`  
Interactive API docs at `http://localhost:8000/docs`

### Frontend Setup

```bash
cd careerbuddy-ai/frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Start dev server
npm run dev
```

Frontend will be live at `http://localhost:5173`

---

## 🌐 Deployment

| Service | Platform | Configuration |
|---|---|---|
| Backend | [Render](https://render.com) | Root: `backend/`, Build: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`, Start: `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Frontend | [Vercel](https://vercel.com) | Root: `frontend/`, Framework: Vite, Env: `VITE_API_URL=<your-render-url>` |

Add `ANTHROPIC_API_KEY` as an environment variable in Render's dashboard.

---

## ⚠️ Known Limitations

- **Limited training data** — AI recommendations improve with larger datasets
- **Bias in job-market data** — Regular model evaluation and fairness checks are required
- **Resume quality dependency** — Poorly formatted or image-based PDFs may yield incomplete results
- **Dynamic job market** — Skill recommendations may lag behind rapidly evolving roles
- **Internet & compute dependency** — Claude API and sentence-transformers require connectivity

---

## 👥 Team — QUANT 4

| Member | Role | Responsibility |
|---|---|---|
| **Ajay Kumar** | Backend Lead | FastAPI server, PDF parsing, NLP extraction |
| **Samarth Sharma** | AI/ML Engineer | ATS scoring, job matching, skill gap, Claude API |
| **Kaustubh Mishra** | Frontend Lead | React UI, dashboard, AI chat interface |
| **Kartik Khemani** | DevOps & Integration | GitHub, Render deployment, Vercel, CORS & integration |

---

## 📄 License

This project was built for **Hacksagon 2026** at ABV-IIITM. All rights reserved by QUANT 4.